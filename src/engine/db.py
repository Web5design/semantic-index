import  os, sys, subprocess

p = os.path.abspath(os.path.dirname(__file__))
if(os.path.abspath(p+"/..") not in sys.path):
	sys.path.append(os.path.abspath(p+"/.."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
from server.models import *


'''
@author: anant bhardwaj
@date: Dec 8, 2012

Actual Schema

'''
class EventInstance:
	def __init__(self, reset=True):
		if(reset):
			Event.objects.all().delete()
			Action.objects.all().delete()
			Noun.objects.all().delete()
			Adverb.objects.all().delete()
			Adjective.objects.all().delete()
		self.e = Event()
		self.e.save()
	
	
	def insert_action(self, action):
		_action = None
		try:
			_action = Action.objects.get(name = action)
		except Action.DoesNotExist:
			_action = Action(name= action)
			_action.save()
		_eaction = EventAction(action = _action, event = self.e)
		_eaction.save()
		return _action
	
		
	def insert_agent(self, agent):
		_agent = agent
		try:
			_agent = Noun.objects.get(name = agent)
		except Noun.DoesNotExist:
			_agent = Noun(name=agent)
			_agent.save()
		_eagent = EventAgent(agent = _agent, event = self.e)
		_eagent.save()
		return _agent
	
	
	
	def insert_patient(self, patient):
		_patient = None
		try:
			_patient = Noun.objects.get(name = patient)
		except Noun.DoesNotExist:
			_patient = Noun(name= patient)
			_patient.save()
		_epatient = EventPatient(patient = _patient, event = self.e)
		_epatient.save()
		return _patient
		
	
	
	def insert_beneficiary(self, beneficiary, action):
		_beneficiary = None
		try:
			_beneficiary = Noun.objects.get(name = beneficiary)
		except Noun.DoesNotExist:
			_beneficiary = Noun(name= beneficiary)
			_beneficiary.save()
		_ebeneficiary = EventBenificiary(beneficiary = _beneficiary, action = action, event = self.e)
		_ebeneficiary.save()
		return _beneficiary
		
	
	
	def insert_instrument(self, instrument, action):
		_instrument = None
		try:
			_instrument = Noun.objects.get(name = instrument)
		except Noun.DoesNotExist:
			_instrument = Noun(name= instrument)
			_instrument.save()
		_einstrument = EventInstrument(instrument = _instrument, action = action, event = self.e)
		_einstrument.save()
		return _instrument
		
	
	
	def insert_location(self, location, action):
		_location = None
		try:
			_location = Noun.objects.get(name = location)
		except Noun.DoesNotExist:
			_location = Noun(name= location)
			_location.save()
		_elocation = EventLocation(location = _location, action = action, event = self.e)
		_elocation.save()
		return _location
	
	
	
	
		
	def insert_time(self, time, action):
		_time = None
		try:
			_time = Noun.objects.get(name = time)
		except Noun.DoesNotExist:
			_time = Noun(name= time)
			_time.save()
		_etime = EventTime(time = _time, action = action, event = self.e)
		_etime.save()
		return _time
	
	
	
	
	def insert_adjective(self, adjective, noun):
		_adjective = None
		try:
			_adjective = Adjective.objects.get(name = adjective)
		except Adjective.DoesNotExist:
			_adjective = Adjective(name= adjective)
			_adjective.save()
		_eadjective = EventAdjective(adjective = _adjective, noun = noun, event = self.e)
		_eadjective.save()
		return _adjective
	
	
	
	def insert_adverb(self, adverb, action):
		_adverb = None
		try:
			_adverb = Adverb.objects.get(name = adverb)
		except Adverb.DoesNotExist:
			_adverb = Adverb(name= adverb)
			_adverb.save()
		_eadverb = EventAdverb(adverb = _adverb, action = action, event = self.e)
		_eadverb.save()
		return _adverb
	
		
		
		


class EventQuery:
	def __init__(self):
		self.event = None
	
	def search_action(self, action):
		res = {}
		action = Action.objects.get(name=action)	
		event_actions = EventAction.objects.filter(action = action)
		res['events']=[]
		for e in event_actions:
			event = {}
			event['id'] = e.event_id
			event['agents'] = [{'agent': ea.agent.name} for ea in EventAgent.objects.filter(event = e.event)]
			event['patients'] = [{'patient': ep.patient.name} for ep in EventPatient.objects.filter(event = e.event)]
			event['beneficiaries'] = [{'beneficiary':eb.beneficiary.name} for ea in EventBeneficiary.objects.filter(event = e.event)]
			event['locations'] = [{'location':el.location.name, 'action':el.action.name} for el in EventLocation.objects.filter(event = e.event)]
			event['time'] = [{'time':et.time.name, 'action':et.action.name} for et in EventTime.objects.filter(event = e.event)]
			event['instruments'] = [{'instrument':ei.instrument.name, 'action':ei.action.name} for ei in EventInstrument.objects.filter(event = e.event)]
			event['adverbs'] = [{'adverb':ea.adverb.name, 'action':ea.action.name} for ea in EventAdverb.objects.filter(event = e.event)]
			event['adjectives'] = [{'adjective':ea.adjective.name, 'noun':ea.noun.name} for ea in EventAdjective.objects.filter(event = e.event)]
			res['events'].append(event)
		return res
		
	def get_tree(self):
		res = {'name':'root'}
		res['children']=[]
		actions = Action.objects.all()
		for action in actions:
			events = {'name':action.name, 'children':[]}
			event_actions = EventAction.objects.filter(action = action)
			i = 1
			for e in event_actions:
				event = {'name':i, 'children':[]}
				agents = [{'name': ea.agent.name} for ea in EventAgent.objects.filter(event = e.event)]
				if(len(agents)> 0):
					event['children'].append({'name':'agent', 'children':agents})
				patients = [{'name': ep.patient.name} for ep in EventPatient.objects.filter(event = e.event)]
				if(len(patients)> 0):
					event['children'].append({'name':'patients', 'children':patients})
				beneficiaries = [{'name':eb.beneficiary.name} for ea in EventBeneficiary.objects.filter(event = e.event)]
				if(len(beneficiaries)> 0):
					event['children'].append({'name':'beneficiaries', 'children':beneficiaries})
				locations = [{'name':el.location.name, 'action':el.action.name} for el in EventLocation.objects.filter(event = e.event)]
				if(len(locations)> 0):
					event['children'].append({'name':'locations', 'children':locations})
				time = [{'name':et.time.name, 'action':et.action.name} for et in EventTime.objects.filter(event = e.event)]
				if(len(time)> 0):
					event['children'].append({'name':'time', 'children':time})
				instruments = [{'name':ei.instrument.name, 'action':ei.action.name} for ei in EventInstrument.objects.filter(event = e.event)]
				if(len(instruments)> 0):
					event['children'].append({'name':'instruments', 'children':instruments})
				adverbs = [{'name':ea.adverb.name, 'action':ea.action.name} for ea in EventAdverb.objects.filter(event = e.event)]
				if(len(adverbs)> 0):
					event['children'].append({'name':'adverbs', 'children':adverbs})
				adjectives = [{'name':ea.adjective.name, 'noun':ea.noun.name} for ea in EventAdjective.objects.filter(event = e.event)]
				if(len(adjectives)> 0):
					event['children'].append({'name':'adjectives', 'children':adjectives})
				events['children'].append(event)
				i += 1
			res['children'].append(events)
		return res	
	
		
if __name__ == "__main__":
	e = EventInstance()
	agent1 = e.insert_agent('John')
	agent2 = e.insert_agent('Josh')
	action = e.insert_action('cut')
	patient = e.insert_patient('the mango')
	instrument = e.insert_instrument('with a knife', action)
	time = e.insert_time('on 5 pm', action)
	location = e.insert_location('at Stata Center', action)
	adj1 = e.insert_adjective('Hungry', agent1)
	adj2 = e.insert_adjective('angry', agent2)
	adv = e.insert_adverb('properly', action)
	
	e = EventInstance(reset=False)
	agent1 = e.insert_agent('Ravi')
	agent2 = e.insert_agent('Ekatrina')
	action = e.insert_action('cut')
	patient = e.insert_patient('the apple')
	instrument = e.insert_instrument('with a fork', action)
	time = e.insert_time('on Tuesday', action)
	location = e.insert_location('at Berwicks ofice', action)
	adj1 = e.insert_adjective('Hungry', agent1)
	adj2 = e.insert_adjective('angry', agent2)
	adv = e.insert_adverb('properly', action)
	
	
	q = EventQuery()
	res = q.search_action('cut')
	print res
	res = q.get_tree()
	print res