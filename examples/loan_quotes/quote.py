#! /usr/bin/python
"""Get quotes for loans.

Module containing tools for getting quotes for loans after processing
input lenders offers which are stored in a minheap for real time access.
Methodology:
  1. Read lenders csv data file
  2. Store lender Offer objects in min heap. A minimum element has either
     smaller rate value or equal rate value but greater available amount
     compared to another element.
  3. Get a quote by using min Offers first.
  4. Print the quote or inform user on an error case.
"""

import sys
import heapq

from itertools import imap,\
                      izip,\
                      starmap,\
                      repeat


class Offer(object):
    """Object representing lenders loan offer

    Args:
        lender: <string> name of lender
        rate: <float> loan's rate value for lender
        loan: <int> available amout tp be loaned
    """
    __slots__ = ['lender', 'rate', 'avail']

    def __init__(self, lender, rate, avail):
        self.lender = lender
        self.rate = float(rate)
        self.avail = int(avail)

    def __lt__(self, other):
        # A minimum offer is considered the one with smaller rate value,
        # or in case of an equal value the one with greater amount available.
        # That is done to involve as less lenders possible in same quote.
        if self.rate == other.rate:
            return self.avail > other.avail
        return self.rate < other.rate

    def __repr__(self):
        return "Offer(%s)" % ':'.join((str(getattr(self, a))
                                       for a in self.__slots__))


class Quote(object):
    """Object represending a quote request for loan

    Args:
        request: <int> loan request amount
        offers: <list> containing offer objects involved in the quote
        months: <int> numbers of months for repayment
    """
    __slots__ = ['request', 'rate', 'monthly', 'total', 'offers']

    def __init__(self, request, offers, months):
        self.request = request
        self.offers = offers

        # Calculate average rate for quote composed by multiple offers
        self.rate = sum(imap(lambda o: o.rate*o.avail, offers))/request

        # Calculate total monthly repayment amount for loan
        monthly = sum(starmap(self.get_monthly_pay,
                              izip(offers, repeat(months))))
        self.monthly = monthly
        self.total = monthly * months

    def get_message(self):
        """String message for command line quote retrieval

        Returns:
            <string> message
        """
        return u"Requested amount: \xA3%4d\n"\
               u"Rate: %.1f%%\n"\
               u"Monthly repayment: \xA3%.2f\n"\
               u"Total repayment: \xA3%.2f\n" %\
               (self.request, self.rate*100, self.monthly, self.total)

    @staticmethod
    def get_monthly_pay(offer, months):
        """Calculates monthly repayment for an offer

        Args:
            offer: <Offer> lenders offer object
            months: <int> number of months for repayment

        Returns:
            <float> monthly repayment
        """
        avail = offer.avail
        rate = offer.rate
        return avail*(rate/12)/(1-(1+rate/12)**-months)


class QuoteException(Exception):
    """On quote retrieval inability"""
    pass


def get_quote(lenders_data, request, months):
    """Get a quote for a loan request.

    Args:
        lenders_data: <list> min heap with lender <Offer> objects
        request: <int> amount of loan request
        months: <int> number of months for repayment

    Returns:
        <Quote> object containing quote information for the given request
    """
    amount_remain = request
    offers = []
    while True:
        try:
            # Get next minimun offer from lenders heap
            offer = heapq.heappop(lenders_data)
            offers.append(offer)

            # If not all available amount by lender is needed to form the
            # quote, add to quote the amount needed and push the rest back
            # to the min heap.
            if offer.avail > amount_remain:
                new_offer = Offer(offer.lender, offer.rate,
                                  offer.avail-amount_remain)
                heapq.heappush(lenders_data, new_offer)
                offer.avail = amount_remain
            amount_remain -= offer.avail
        except IndexError:
            # All heap items are processed without gathering amount needed
            raise QuoteException('Request amount bigger than total offers')
        if amount_remain == 0:
            break
    return Quote(request, offers, months)


def get_lenders_data(lenders_file):
    """Get lenders offers

    Returns:
        <list> min heap containing lender <Offer> objects
    """
    lenders_data = []
    with open(lenders_file, 'r') as fobj:
        fobj.readline()
        for line in fobj:
            line = line.strip().split(',')
            lenders_data.append(Offer(line[0], line[1], line[2]))
    heapq.heapify(lenders_data)
    return lenders_data


if __name__ == '__main__':  # pragma: no cover
    class InputArgsException(Exception):
        """In case of wrong user input arguments"""
        pass

    EXITCODE = 0
    try:
        if len(sys.argv) != 3:
            raise InputArgsException('Wrong arguments number')
        LENDERSFILE = sys.argv[1]
        LOAN = int(sys.argv[2])
        if (1000 <= LOAN <= 15000) is False or\
           LOAN % 100 != 0:
            raise InputArgsException('Invalid loan amount request')

        # Get quote and print quote message for requested loan amount.
        MONTHSREPAY = 36
        QUOTE = get_quote(get_lenders_data(LENDERSFILE), LOAN, MONTHSREPAY)
        print QUOTE.get_message()

    except InputArgsException as exc:
        print exc
        print "USAGE: <exe> <lenders file> <loan amount>"
        EXITCODE = 1

    except (IOError, ValueError) as exc:
        print "%s - %s" % (exc.__class__.__name__, exc)
        EXITCODE = 1

    except QuoteException as exc:
        print "Unable to provide quote - %s" % (exc)
        EXITCODE = 1

    sys.exit(EXITCODE)
