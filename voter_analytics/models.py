from django.db import models
import csv
from datetime import datetime

class Voter(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=50)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}, Precinct: {self.precinct_number}"

    @staticmethod
    def load_data():
        """Load data records from a CSV file into Voter model instances."""
        Voter.objects.all().delete()
        filename = '/Users/noahcolbert/Desktop/django/newton_voters.csv'

        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            print(headers)

            for line in reader:
                try:
                    voter = Voter(
                        last_name=line[1],
                        first_name=line[2],
                        street_number=line[3],
                        street_name=line[4],
                        apartment_number=line[5] if line[5] else None,
                        zip_code=line[6],
                        date_of_birth=datetime.strptime(line[7], '%Y-%m-%d').date(),
                        date_of_registration=datetime.strptime(line[8], '%Y-%m-%d').date(),
                        party_affiliation=line[9].strip(" "),
                        precinct_number=str(line[10]),
                        v20state=line[11] == 'TRUE',
                        v21town=line[12] == 'TRUE',
                        v21primary=line[13] == 'TRUE',
                        v22general=line[14] == 'TRUE',
                        v23town=line[15] == 'TRUE',
                        voter_score=int(line[16]),
                    )
                    voter.save()
                    print(f'Created voter: {voter}')
                
                except Exception as e:
                    print(f"Exception on line {line}: {e}")
