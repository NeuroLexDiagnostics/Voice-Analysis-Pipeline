from DigiPsych_API.lang_check.coherence_master import coherence
import os
import collections

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def coherenceMeasure(txt):
	coh = coherence.coherenceAnalisys()
	res = coh.analysis_text(txt)
	return res

def coherenceMeasureOutput(path):
	with open(path, encoding = "utf-8", errors='ignore') as word_list:
		rawText = word_list.read()
		inputTranscript = rawText.split(' ')
	return [path, flatten(coherenceMeasure(rawText))]