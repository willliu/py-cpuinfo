

import unittest
from cpuinfo import cpuinfo


class DataSource(object):
	bits = '32bit'
	cpu_count = 1
	is_windows = False
	raw_arch_string = 'armv7l'

	@staticmethod
	def has_proc_cpuinfo():
		return True

	@staticmethod
	def has_cpufreq_info():
		return True

	@staticmethod
	def cat_proc_cpuinfo():
		returncode = 0
		output = '''
processor       : 0
model name      : ARMv6-compatible processor rev 7 (v6l)
Features        : swp half thumb fastmult vfp edsp java tls 
CPU implementer : 0x41
CPU architecture: 7
CPU variant     : 0x0
CPU part        : 0xb76
CPU revision    : 7

Hardware        : BCM2708
Revision        : 0010
Serial          : 00000000be6d9ba0


'''
		return returncode, output


	@staticmethod
	def cpufreq_info():
		returncode = 0
		output = '''
cpufrequtils 008: cpufreq-info (C) Dominik Brodowski 2004-2009
Report errors and bugs to cpufreq@vger.kernel.org, please.
analyzing CPU 0:
driver: generic_cpu0
CPUs which run at the same hardware frequency: 0
CPUs which need to have their frequency coordinated by software: 0
maximum transition latency: 300 us.
hardware limits: 300 MHz - 1000 MHz
available frequency steps: 300 MHz, 600 MHz, 800 MHz, 1000 MHz
available cpufreq governors: conservative, ondemand, userspace, powersave, performance
current policy: frequency should be within 300 MHz and 1000 MHz.
The governor "performance" may decide which speed to use
within this range.
current CPU frequency is 1000 MHz.
cpufreq stats: 300 MHz:0.00%, 600 MHz:0.00%, 800 MHz:0.00%, 1000 MHz:100.00%
'''
		return returncode, output


class TestBeagleBone(unittest.TestCase):
	def test_all(self):
		cpuinfo.DataSource = DataSource

		info = cpuinfo.get_cpu_info_from_proc_cpuinfo()

		self.assertEqual('', info['vendor_id'])
		self.assertEqual('BCM2708', info['hardware'])
		self.assertEqual('ARMv6-compatible processor rev 7 (v6l)', info['brand'])
		self.assertEqual('1.0000 GHz', info['hz_advertised'])
		self.assertEqual('1.0000 GHz', info['hz_actual'])
		self.assertEqual((1000000000, 0), info['hz_advertised_raw'])
		self.assertEqual((1000000000, 0), info['hz_actual_raw'])
		self.assertEqual('ARM_7', info['arch'])
		self.assertEqual(32, info['bits'])
		self.assertEqual(1, info['count'])

		self.assertEqual('armv7l', info['raw_arch_string'])

		self.assertEqual('', info['l2_cache_size'])
		self.assertEqual(0, info['l2_cache_line_size'])
		self.assertEqual(0, info['l2_cache_associativity'])

		self.assertEqual(0, info['stepping'])
		self.assertEqual(0, info['model'])
		self.assertEqual(0, info['family'])
		self.assertEqual(0, info['processor_type'])
		self.assertEqual(0, info['extended_model'])
		self.assertEqual(0, info['extended_family'])
		self.assertEqual(
			['edsp', 'fastmult', 'half', 'java', 'swp', 'thumb', 'tls', 'vfp']
			,
			info['flags']
		)





