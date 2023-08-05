#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 20:01:29 2022

@author: m102324
"""
import unittest
from cobindability.BED import *

class TestBED(unittest.TestCase):

	def test_union_bed3(self):
		input_data = [('chr1', 1, 10), ('chr1', 3, 15), ('chr1', 20, 35), ('chr1', 20, 50)]
		output = [('chr1', 1, 15), ('chr1', 20, 50)]
		self.assertEqual(union_bed3(input_data), output, "Should be [('chr1', 1, 15), ('chr1', 20, 50)]")

	def test_intersect_bed3(self):
		input_data1 = [('chr1', 1, 10), ('chr1', 20, 35)]
		input_data2 = [('chr1',3, 15), ('chr1',20, 50)]
		output = [('chr1', 3, 10), ('chr1', 20, 35)]
		self.assertEqual(intersect_bed3(input_data1, input_data2), output, "Should be [('chr1', 3, 10), ('chr1', 20, 35)]")

	def test_subtract_bed3(self):
		input_data1 = [('chr1', 1, 10), ('chr1', 20, 35)]
		input_data2 = [('chr1',3, 15), ('chr1',20, 50)]
		output = [('chr1', 1, 3)]
		self.assertEqual(subtract_bed3(input_data1, input_data2), output, "Should be [('chr1', 1, 3)]")


	def test_bed_actual_size(self):
		input_data1 = [('chr1', 1, 10), ('chr1', 20, 35)]
		input_data2 = [('chr1',3, 15), ('chr1',20, 50)]
		output = [24, 42]
		self.assertEqual(bed_actual_size(input_data1, input_data2), output, "Should be [24, 42]")

	def test_bed_counts(self):
		input_data1 = [('chr1', 1, 10), ('chr1', 20, 35)]
		input_data2 = [('chr1',3, 15), ('chr1',20, 50), ('chr2',100,200)]
		output = [2, 3]
		self.assertEqual(bed_counts(input_data1, input_data2), output, "Should be [2, 3]")

	def test_bed_genomic_size(self):
		input_data1 = [('chr1', 0, 100), ('chr1', 50, 150), ('chr1', 80, 180)]
		input_data2 = [('chr1', 0, 100), ('chr2', 50, 150), ('chr3', 80, 180)]
		output = [180, 300]
		self.assertEqual(bed_genomic_size(input_data1, input_data2), output, "Should be [180, 300]")

	def test_bed_overlap_size(self):
		input_data1 = [('chr1', 1, 10), ('chr1', 20, 35)]
		input_data2 = [('chr1',3, 15), ('chr1',20, 50)]
		output = 22
		self.assertEqual(bed_overlap_size(input_data1, input_data2), output, "Should be 22")

	def test_is_overlap(self):
		self.assertEqual(is_overlap('chr1', 1, 100, 'chr1', 50, 150), 50, "Should be 50")

if __name__ == '__main__':
	unittest.main()