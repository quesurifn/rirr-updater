# Architecture

<object data="assets/ip_source.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="assets/ip_source.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="assets/ip_source.pdf">Download PDF</a>.</p>
    </embed>
</object>

# To run 

- Install the dependencies

- Run MongoDB and Rabbit MQ locally

- Wait until 12am system time

- The job will kick off to download all allocated IP blocks via the 5 RIRs.

- Log into the Rabbit MQ panel to see the queue fill up with over 100k ip blocks

- Run the consumer with Python `python consumer/consumer.py` consumer will start, download the IP owner's information (company) for each allocated block
 and save to MongoDB




