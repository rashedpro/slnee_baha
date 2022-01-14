# Copyright (c) 2022 , Slnee 
# MIT License. See license.txt


from __future__ import unicode_literals
from typing import Optional
import frappe
import operator
import json
import base64
import re, datetime, math, time
from six.moves.urllib.parse import quote, urljoin
from six import iteritems, text_type, string_types, integer_types
from code import compile_command
from frappe.desk.utils import slug
from click import secho
from num2words import num2words


number_format_info = {
	"#,###.##": (".", ",", 2),
	"#.###,##": (",", ".", 2),
	"# ###.##": (".", " ", 2),
	"# ###,##": (",", " ", 2),
	"#'###.##": (".", "'", 2),
	"#, ###.##": (".", ", ", 2),
	"#,##,###.##": (".", ",", 2),
	"#,###.###": (".", ",", 3),
	"#.###": ("", ".", 0),
	"#,###": ("", ",", 0),
	"#.########": (".", "", 8)
}
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S.%f"
DATETIME_FORMAT = DATE_FORMAT + " " + TIME_FORMAT

@frappe.whitelist()
def get_fields(doctype):
	fields = frappe.get_doc("DocType",doctype).fields
	r=[]
	for f in fields :
		if f.label!= None and f.fieldtype not in ["Table","Section Break","Column Break"]:
			r.append(f.fieldname)
	r.append("name")
	r.append("page_number")
	r.sort()
	r.insert(0,"")
	return(r)
@frappe.whitelist()
def get_table_fields(doctype):
        fields = frappe.get_doc("DocType",doctype).fields
        r=[]
        for f in fields :
                if f.label!= None and f.fieldtype == "Table":
                        r.append(f.fieldname)
        r.sort()
        r.insert(0,"")
        return(r)

@frappe.whitelist()
def get_fonts():
	return (frappe.db.get_list('Font', pluck='name',order_by='name asc'))

@frappe.whitelist()
def get_cells(prin,div):
	lines=frappe.db.get_value("div",div,"table_lines")
	columns=frappe.db.get_value("div",div,"table_columns")
	table=[]
	print(prin,div,lines,columns)
	for l in range(1,lines+1):
		line=[]
		for c in range(1,columns+1):
			c= frappe.db.get_list('cell',filters={'parent':prin,'div':div,"line":l,"column":c})
			#c = [None] if len(c)==0
			if len(c)!=0:
				doc = frappe.get_doc('cell', c[0]["name"])
			else:
				doc=None
			line.append(doc)
		table.append(line)
	print(table)
	return(table)



def money_in_words(number, main_currency = None, fraction_currency=None):
        """
        Returns string in words with currency and fraction currency.
        """
        from frappe.utils import get_defaults
        _ = frappe._

        try:
                # note: `flt` returns 0 for invalid input and we don't want that
                number = float(number)
        except ValueError:
                return ""

        number = flt(number)
        if number < 0:
                return ""

        d = get_defaults()
        if not main_currency:
                main_currency = d.get('currency', 'INR')
        if not fraction_currency:
                fraction_currency = frappe.db.get_value("Currency", main_currency, "fraction", cache=True) or _("Cent")

        number_format = frappe.db.get_value("Currency", main_currency, "number_format", cache=True) or \
                frappe.db.get_default("number_format") or "#,###.##"

        fraction_length = get_number_format_info(number_format)[2]
        n = "%.{0}f".format(fraction_length) % number

        numbers = n.split('.')
        main, fraction =  numbers if len(numbers) > 1 else [n, '00']

        locale="en_EN"
        anda="and"
        zero="zero"
        if main_currency=="ريال سعودي" or main_currency=="ريال":
                locale="ar_AR"
                anda="و"
                zero="صفر"

        if len(fraction) < fraction_length:
                zeros = '0' * (fraction_length - len(fraction))
                fraction += zeros

        in_million = True
        if number_format == "#,##,###.##": in_million = False

        # 0.00
        if main == '0' and fraction in ['00', '000']:
                out = "{1} {0}".format(main_currency, zero)
        # 0.XX
        elif main == '0':
                out = _(in_words(fraction, in_million,locale).title()) + ' ' + fraction_currency
        else:
                out = _(in_words(main, in_million,locale).title()) +' '+ main_currency
                if cint(fraction):
                        out = out + ' ' + anda+ ' ' + _(in_words(fraction, in_million,locale).title()) + ' ' + fraction_currency

        return out 

#
# convert number to words
#
def in_words(integer, in_million=True,lang=None):
        """
        Returns string in words for the given integer.
        """
        locale = lang if lang else frappe.local.lang
        integer = int(integer)
        try:
                ret = num2words(integer, lang=locale)
        except NotImplementedError:
                ret = num2words(integer, lang='en')
        except OverflowError:
                ret = num2words(integer, lang='en')
        return ret.replace('-', ' ')


def cint(s, default=0):
	"""Convert to integer
		:param s: Number in string or other numeric format.
		:returns: Converted number in python integer type.
		Returns default if input can not be converted to integer.
		Examples:
		>>> cint("100")
		100
		>>> cint("a")
		0
	"""
	try:
		return int(float(s))
	except Exception:
		return default
def flt(s, precision=None):
	"""Convert to float (ignoring commas in string)
		:param s: Number in string or other numeric format.
		:param precision: optional argument to specify precision for rounding.
		:returns: Converted number in python float type.
		Returns 0 if input can not be converted to float.
		Examples:
		>>> flt("43.5", precision=0)
		44
		>>> flt("42.5", precision=0)
		42
		>>> flt("10,500.5666", precision=2)
		10500.57
		>>> flt("a")
		0.0
	"""
	if isinstance(s, str):
		s = s.replace(',','')

	try:
		num = float(s)
		if precision is not None:
			num = rounded(num, precision)
	except Exception:
		num = 0.0

	return num

def get_number_format_info(format):
	return number_format_info.get(format) or (".", ",", 2)
