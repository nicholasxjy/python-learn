import collections
import sys
import math
Statistics = collections.namedtuple("Statistics", "mean mode median std_dev")

def main():
	if len(sys.argv) == 1 or sys.argv[1] in ["-h", "--help"]:
		print("usage:{0}file1[file2[...fileN]]".format(sys.argv[0]))
		sys.exit()

	numbers = []
	frequences = collections.defaultdict(int)
	for filename in sys.argv[1:]:
		read_data(filename, numbers, frequences)
	if numbers:
		statistics = calculate_statistics(numbers, frequences)
		print_results(len(numbers), statistics)
	else:
		print("no numbers found")

def read_data(filename, numbers, frequences):
	for lino, line in enumerate(open(filename, encoding="ascii"), start=1):
		for x in line.split():
			try:
				number = float(x)
				numbers.append(number)
				frequences[number] = frequences.get(number,0)+1
			except ValueError as err:
				print("{filename}:{lino}:skipping{x}:{err}".format(**locals()))

def calculate_statistics(numbers, frequences):
	mean = sum(numbers)/len(numbers)
	mode = calculate_mode(frequences, 3)
	median = calculate_median(numbers)
	std_dev = calculate_std_dev(numbers, mean)
	return Statistics(mean, mode, median, std_dev)

def calculate_mode(frequences, maximum_modes):
	highest_frequency = max(frequences.values())
	mode = [number for number, frequency in frequences.items() if frequency == highest_frequency]
	if not(1 <= len(mode) <= maximum_modes):
		mode = None
	else:
		mode.sort()
	return mode

def calculate_median(numbers):
	numbers = sorted(numbers)
	middle = len(numbers)/2
	median = numbers[middle]
	if len(numbers) % 2 == 0:
		median = (median + numbers[middle - 1])/2
	return median

def calculate_std_dev(numbers, mean):
	total = 0
	for number in numbers:
		total += ((number - mean) ** 2)
	variance = total/(len(numbers) -1)
	return math.sqrt(variance)

def print_results(count, statistics):
	real = "9.2f"
	if statistics.mode is None:
		modeline = ""
	elif len(statistics.mode) == 1:
		modeline = "mode     = {0:{fmt}}\n".format(statistics.mode[0], fmt=real)
	else:
		modeline = ("mode    = [" + ",".join(["{0:.2f".format(m) for m in statistics.mode]) + "]\n")
	print("""\
		count   = {0:6}
		mean    = {mean:{fmt}}
		median  = {median:{fmt}}
		{1}\
		std.dev. = {std_dev:{fmt}""".format(count, modeline, fmt=real, **statistics._asdict()))