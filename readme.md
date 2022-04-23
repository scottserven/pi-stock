Design:

## Requirements

We want to have a list of product page URLs that are continually checked at a 
specified frequency, and when one or matches is found, alert a Discord channel.  

Upon alerting a given URL, that URL should not be re-alerted for a certain period of 
time, so that it does not spam the channel.

If a URL was alerted on for availability, and a subsequent check indicates it is
out of stock, the "out of stock" status should be alerted, and that URLs re-alert
timer should be reset so that it alerts the next time any stock is detected.