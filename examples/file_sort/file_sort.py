#!/usr/bin/python
"""Module containing tools for applying sorting operations in files."""

import os
import sys
import heapq
import tempfile

from sorting_methods import quicksort,\
                            merge_sort,\
                            default_sort


class InitializeError(Exception):
    """Exception to be raised in case of incorrect initialization."""
    pass


class SortingError(Exception):
    """Exception to be raised in case of an error while performing
    the sorting operation."""
    pass


class FileSorter(object):
    """
    Description:
        Object for sorting the contents of a given input file that contains
        numbers. Sorting can be done in various ways by selecting different
        sorting public method or providing custom sorting functions.

    Input:
        input_file: <string> path of a file containing numbers(one if a row)

    Raises:
        InitializeError: on invalid initialization process.
    """
    def __init__(self, input_file):
        if os.path.isfile(input_file) is False:
            raise InitializeError('"%s" file does not exist' % (input_file))

        # Output file should have a value other than None only if the
        # result contents are writen successfully.
        self._output_file = None
        self._input_file = input_file

    def sort(self, sort_method=None):
        """
        Description:
            Method for sorting the contents of an input file and creates
            an output file with the sorted contents.

        Input:
            [sort_method]: <function> sorting function to be used instead
                            of default.
        """
        if sort_method is None:
            sort_method = default_sort

        # Create a list containing the integer numbers found in input file.
        with open(self._input_file, 'r') as fobj:
            itemslist = [i for i in self._ints_from_fileobj(fobj)]

        # Sort the list.
        sort_method(itemslist)

        # Create the output file that contains sorted contents.
        self._output_file = '%s.sorted' % (self._input_file)
        with open(self._output_file, 'w') as fobj:
            self._ints_to_fileobj(fobj, iter(itemslist))

    def external_sort(self, itemslimit, sort_method=None):
        """
        Description:
            Method for sorting the contents of an input file and creates
            an output file with the sorted contents by having a restriction
            of maximum items that an be loaded to memory at each time. The
            process that is being followed to achieve that is:
              1. Create intermediate files with size up to the memory limit.
              2. Sort these intermediate files.
              3. Merge them into the output result file.

        Input:
            itemslimit: <integer> limit of items can be loaded to memory
                         simultaneously.
            [sort_method]: <function > sorting function to be used instead
                            of default. Must apply an in place sort and not
                            use any additional memory.

        Raises:
            SortingError: while doing sorting operations.
            IOError: while doing file operations.
        """
        if sort_method is None:
            sort_method = quicksort
        if isinstance(itemslimit, int) is False or itemslimit < 1:
            raise SortingError('Invalid itemslimit param: "%s"' % (itemslimit))

        # Initialize the memory will be used to load the numbers by using
        # int_loader as a generator that will be yielding them.
        itemslist = []
        in_fobj = open(self._input_file, 'r')
        int_loader = self._ints_from_fileobj(in_fobj)

        # Store open file handles of temporary sorted files.
        sorted_files_gens = []
        loop = True
        while loop:
            try:
                # Load next number from input file's generator method.
                num = int_loader.next()
                itemslist.append(num)
            except StopIteration:
                in_fobj.close()
                loop = False

            # If the memory list contains numbers just before exiting the loop
            # or the memory list capacity reached our given limit,
            # then create a sorted temporary file and store in a list a
            # generator for retrieving the values later.
            if (len(itemslist) == itemslimit) or (loop is False and itemslist):
                sort_method(itemslist)
                fobj = tempfile.TemporaryFile()
                self._ints_to_fileobj(fobj, iter(itemslist))

                # Store open file handler pointing the start of sorted file.
                fobj.seek(0)
                sorted_files_gens.append(self._ints_from_fileobj(fobj))
                del itemslist[:]

                # In case that memory limit is too low to handle the merge
                # of the temporary files.
                if len(sorted_files_gens) > itemslimit/2:
                    raise SortingError('Merge %d temp files with limit %d' %
                                       (len(sorted_files_gens), itemslimit))
        if len(itemslist):
            raise SortingError('Not all numbers saved in tmp files')

        # If one or more temporary sorted file generators are being stored
        # then merge them into result file.
        if sorted_files_gens:
            self._merge_sorted_files(itemslist, sorted_files_gens, itemslimit)

    def _merge_sorted_files(self, itemslist, sorted_files_gens, itemslimit):
        """
        Description:
            Merge a list that contains generators that will be yielding values
            from the intermediate temporary sorted files. The process that is
            being followed is:
              1. Load into memory equal parts of numbers from the generators.
              2. Dump a part of that size with the smallest numbers to the
                 output file.
              3. Load into memory numbers from the generators that was
                 originally contained the numbers dumped in step 2.

        Input:
            itemslist: <list> with limitted number of items to simultaneously
                               contain.
            sorted_files_gens: <list> that contains generators to sorted files
            itemslimit: <integer> - max number of items stored in itemslist.
        """

        # Set the number of ints to be stored in items list from each sorted
        # temporary source file.
        ints_per_chunk = itemslimit/len(sorted_files_gens)
        for int_gen in sorted_files_gens:
            for _ in xrange(ints_per_chunk):
                try:
                    num = int_gen.next()
                    itemslist.append((num, int_gen))
                except StopIteration:
                    continue

        # Start writing into the output file as the smaller numbers are found
        # by using a heap that contains tuple objects for storing the source
        # generator object that is linked to it's generated value.
        self._output_file = '%s.sorted' % (self._input_file)
        with open(self._output_file, 'w') as fobj:
            while len(itemslist):
                heapq.heapify(itemslist)
                for _ in xrange(min(len(itemslist), ints_per_chunk)):
                    num, int_gen = heapq.heappop(itemslist)
                    fobj.write('%d\n' % (num))
                    try:
                        num = int_gen.next()
                        itemslist.append((num, int_gen))
                    except StopIteration:
                        pass

    @staticmethod
    def _ints_from_fileobj(fobj):
        """
        Description:
            Generator method for yielding integers found by using a file object

        Input:
            fobj: <file object> by a file opened with read permissions.
        """
        for line in fobj:
            yield int(line.strip('\n'))

    @staticmethod
    def _ints_to_fileobj(fobj, items):
        """
        Description:
            Method for writing integers to a file by using it's file object.

        Input:
            fobj: <file object> by a file opened with write permissions.
            items: <iterator> to be used for retrieving the desired ints.
        """
        for item in items:
            fobj.write('%d\n' % (item,))

    def get_output_filename(self):
        """
        Description:
            Method for retrieving output file's path if that is successfully
            created.

        Returns:
            output_file: <string> representing the path
                         <None> if output file is not created.
        """
        return self._output_file


if __name__ == '__main__':  # pragma: no cover
    # Description:
    #    Script to read command line arguments and based on that sorts
    #    the contents of a given input file that contains integers.

    class InputArgsError(Exception):
        """Exception to be raised in case of wrong input arguments usage"""

    EXITCODE = 0
    try:
        SORT_TYPES = ('mergesort', 'quicksort', 'external')
        SORT_TYPE = None
        if ('-help' in sys.argv) or len(sys.argv) not in (2, 3):
            raise InputArgsError()
        if len(sys.argv) == 3 and sys.argv[2] not in SORT_TYPES:
            print "Available sort types:\n\t%s" % '\n\t'.join(SORT_TYPES)
            raise InputArgsError(sys.argv[2])
        elif len(sys.argv) == 3:
            SORT_TYPE = sys.argv[2]

        # Create an object that will be used to sort the file.
        FILESORTER = FileSorter(input_file=sys.argv[1])

        # Sort the files based on input arguments.
        if SORT_TYPE is None:
            FILESORTER.sort()
        elif SORT_TYPE == 'mergesort':
            FILESORTER.sort(sort_method=merge_sort)
        elif SORT_TYPE == 'quicksort':
            FILESORTER.sort(sort_method=quicksort)
        elif SORT_TYPE == 'external':
            FILESORTER.external_sort(1000)

        # Display the output file.
        print "Result file: %s" % (FILESORTER.get_output_filename())
    except (IOError, InitializeError, SortingError) as exc:
        print "{} - {}".format(exc.__class__.__name__, exc)
        EXITCODE = 1
    except InputArgsError:
        print "USAGE: <executable> <input file> [<sort type>]"
        EXITCODE = 1

    sys.exit(EXITCODE)
