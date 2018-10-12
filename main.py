import os
import csv
import logging

# This application walks through the images in a folder ('test-images'),
# passes the image through Google Vision API and then stores
# information about the objects that the API sees in the
# iamges in a CSV file.

from do_search import do_safe_search, do_label_detection


logging.basicConfig(filename="csv-walk.log", level=logging.INFO)
logging.info("Started")

# Loop through specified folder/sub-folders to find images
with open("vision_api_responses.csv", "w", newline="") as f:
    # Open csv file for our data and initialise it.
    file_writer = csv.writer(f, delimiter=",", quotechar="'")
    logging.info("Opened CSV file for writing and set parameters")

    for root, dirs, files in os.walk(".\\test-images"):
        print("root: {0}".format(root))
        logging.info("root: {0}".format(root))
        for f in files:
            # Create a new row [list] to store our data and append the root
            # directory
            logging.info("file: " + f)
            logging.info("Creating out_row []")
            out_row = []
            out_row.append(root + "\\" + f)
            print("    File: {0}".format(root + "\\" + f))

            # Do our safe search to check for adult or violent content
            logging.info("Calling Safe Search")
            info, adult, violence = do_safe_search(root + "\\" + f)
            out_row.append(adult)
            out_row.append(violence)

            # Check for labels within our image
            logging.info("Calling label detection")
            labels = do_label_detection(root + "\\" + f)
            for label in labels:
                percent_score = int(label.score * 100)
                out_row.append(label.description)
                out_row.append(percent_score)

            # write out the row to our csv file
            logging.info("Write out_row to CSV file")
            file_writer.writerow(out_row)
