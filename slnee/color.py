from __future__ import print_function
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import frappe
from PIL.ImageOps import grayscale
NUM_CLUSTERS = 5
import requests
import os
import sys

@frappe.whitelist()
def get_color(src=None):
        NUM_CLUSTERS = 5
        if not src or not os.path.exists('site1.local/public'+src):
                frappe.msgprint("An error has occurred while trying to select color! setting color to black.",raise_exception = False)
                return('#000000')
        im=Image.open('site1.local/public'+src)
        im = im.convert("RGBA")
        im = im.resize((150, 150))      # optional, to reduce time
        background = Image.new('RGBA', im.size, (255,255,255))
        im=  Image.alpha_composite(background, im)
        ar = np.asarray(im)
        shape = ar.shape
        ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
        codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
        vecs, dist = scipy.cluster.vq.vq(ar, codes)      # assign codes
        counts, bins = np.histogram(vecs, len(codes))    # count occurrences
        index_max = np.argmax(counts)                    # find most frequent
        counts[index_max]=0
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii') # actual colour, (in HEX)
        #if tha background is white the code will select white , so we eliminate it
        if peak[0] > 250 and peak[1] > 250 and peak[1] > 250:
                index_max = np.argmax(counts)
                peak = codes[index_max]
                colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii') # actual colour, (in HEX)
        return("#"+colour[:6])
def change_color(doc, method):
    if doc.select_color_from_logo:
        col=get_color(doc.company_logo)
        doc.color=col
    return doc
