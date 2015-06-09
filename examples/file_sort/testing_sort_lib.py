"""
Unit test containing testcases for the sorting modules
"""
import os
import random
import tempfile
import unittest

from sorting_methods import quicksort,\
                            merge_sort,\
                            default_sort

from file_sort import FileSorter,\
                      SortingError,\
                      InitializeError


def get_all_perms(int_array, idx=None):
    """
    Description:
        Generator that yields all permutations of an input given list.
        Used for exchaustive testing and corner case hitting of sorting
        methods functionality.
    """
    if idx is None:
        idx = len(int_array)
    if idx == 0:
        yield []
    elif idx == 1:
        yield [int_array[-idx]]
    else:
        for perm in get_all_perms(int_array, idx=idx-1):
            for i in xrange(0, len(perm)+1):
                new_perm = perm[:]
                new_perm.insert(i, int_array[-idx])
                yield new_perm


class SortingTestsBase(unittest.TestCase):
    """
    Description:
        Base class that will be inheritted by sorting testcase classes.
    """
    @classmethod
    def setUpClass(cls):
        cls.lists = []
        cls.lists_tested = 0
        print "Setup class: %s" % (cls.__name__)

    @classmethod
    def tearDownClass(cls):
        print "lists tested: %d\n" % cls.lists_tested

    @staticmethod
    def is_sorted(seq):
        """
        Description:
            Method for testing if the input given list is sorted.

        Args:
            int_array: <iterable> accessed by index containing comparables

        Returns:
            <boolean>: True if is sorted, else False
        """
        if seq:
            prev = seq[0]
            for item in seq:
                if prev > item:
                    return False
                prev = item
        return True


class FileSortTestcase(SortingTestsBase):
    """
    Description:
        Class containing tests for the FileSorter object's functionality.
    """
    @classmethod
    def setUpClass(cls):
        super(FileSortTestcase, cls).setUpClass()
        for lengths in (0, 1, 2, 3, 4):
            cls.lists += list(get_all_perms(range(lengths)))
        big_list = range(1000, 6000) + range(500, 5500)
        random.shuffle(big_list)
        cls.lists.append(big_list)
        cls.lists.append(big_list+[1])

    @staticmethod
    def _create_temporary_input_file(numbers):
        """Create a temporary input file containing numbers from lists

        Args:
            numbers: <iterable> containing <int> objects

        Returns:
            <File Object> closed, to the temporary file created
        """
        fobj = tempfile.NamedTemporaryFile(delete=False)
        for num in numbers:
            fobj.write('%d\n' % (num))
        fobj.close()
        return fobj

    def file_sort_common(self, sort_method=None, itemslimit=False):
        """
        Description:
            Basic common testing function to test sort methods of the
            FileSorter object
        """
        for alist in self.lists:
            fobj = self._create_temporary_input_file(alist)
            file_sort = FileSorter(input_file=fobj.name)

            # In-memory sorting.
            if itemslimit is False:
                file_sort.sort(sort_method=sort_method)

            # External sorting
            else:
                limit = max(1, len(alist)/10)
                try:
                    file_sort.external_sort(limit)
                except SortingError:
                    os.unlink(fobj.name)
                    continue
            os.unlink(fobj.name)

            # In a valid output filename case, test if contents are sorted.
            numbers = None
            output_filename = file_sort.get_output_filename()
            if output_filename is not None:
                with open(output_filename, 'r') as out_fobj:
                    for line in out_fobj:
                        numbers = [int(line.strip('\n')) for line in out_fobj]
                os.remove(output_filename)
                if numbers:
                    self.assertTrue(self.is_sorted(numbers))

            # No output file is acceptable only in an empty input list case.
            else:
                self.assertEqual(len(alist), 0)
            FileSortTestcase.lists_tested += 1

    def test_file_default_sort(self):
        """File sorting with default sorting method"""
        self.file_sort_common(sort_method=None)

    def test_file_quicksort(self):
        """File sorting with the quicksort implementation"""
        self.file_sort_common(sort_method=quicksort)

    def test_file_merge_sort(self):
        """File sorting with the merge sort implementation"""
        self.file_sort_common(sort_method=merge_sort)

    def test_file_external_sort(self):
        """File sorting with the external sorting implementation"""
        self.file_sort_common(itemslimit=True)

    def test_invalid_input_file(self):
        """Test the case of a non existing input file"""
        with self.assertRaises(InitializeError):
            FileSorter('/Not/Exists')

    def test_invalid_itemslimit(self):
        """Test the case of invalid memory limit asked"""
        with self.assertRaises(SortingError):
            fobj = tempfile.NamedTemporaryFile()
            FileSorter(fobj.name).external_sort(0)


class SortingFunctionsTests(SortingTestsBase):
    """
    Description:
        Class containing tests for the collection of the sorting methods.
    """
    @classmethod
    def setUpClass(cls):
        super(SortingFunctionsTests, cls).setUpClass()
        for lengths in (0, 1, 2, 6, 7):
            cls.lists += list(get_all_perms(range(lengths)))

    def test_quicksort(self):
        """Test the quicksort algorithm implementation"""
        self.run_on_lists(quicksort)

    def test_merge_sort(self):
        """Test the merge sort algorithm implementation"""
        self.run_on_lists(merge_sort)

    def test_default_sort(self):
        """Test the default sorting algorithm implementation"""
        self.run_on_lists(default_sort)

    def run_on_lists(self, sort_function):
        """
        Description:
            Test the input given function with lists defined in class setup
            method.
        """
        for alist in self.lists:
            copy = alist[:]
            sort_function(copy)
            self.assertTrue(self.is_sorted(copy))
            SortingFunctionsTests.lists_tested += 1


if __name__ == '__main__':
    unittest.main(verbosity=2)
