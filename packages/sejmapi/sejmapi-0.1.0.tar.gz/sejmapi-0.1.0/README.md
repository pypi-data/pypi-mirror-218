# SejmAPI
Python module to work with polish goverment-run Sejm API
https://api.sejm.gov.pl/

# Short overview
```python
sejm = SejmApi(term=9) #creating SejmApi class object and selecting the term(in this case 9)
```
View list of all MPs
```python
sejm.get_all_MP()
```
Get some details on the MP 
```python
sejm.get_MP_info(leg=1) #leg is the legitimation id
```
Get link to the MP's photo
```python
sejm.getPhoto(leg=1)
```
Get list of clubs
```python
sejm.getClubs()
```
Get info about the club
```python
sejm.getClub_info(id='PiS') #id is the name of the club
```
Get a link to the logo of the club
```python
sejm.getClublogo(id='PiS')
```
Get the list of the committees
```python
 sejm.getCommittees()
```
Get a list of the streams from Sejm
```python
sejm.getStreams()
```
Get streams from today
```python
sejm.getTodayStreams()
```
Get info about a term
```python
sejm.getTermInfo()
```
Get all the prints of the term
```python
sejm.getPrints()
```
Get the print details
```python
sejm.getPrint_info(nr=1) #nr is the nr. of the print
```
Get the link to the attachment to the print
```python
sejm.getPrint_attachment(nr=1,fileName='1.pdf')
``` 
