<h2>Coherence Algorithm</h2>

 
Coherence Algorithm used in *Automated analysis of free speech predicts psychosis onset in high-risk youths*
(<a href="http://www.nature.com/articles/npjschz201530?WT.mc_id=GOP_SCHZ_1508_201530">download the paper</a>) to study the speech coherence level. For now, the algorithm works in English but it is very easy to adapt into others languages.

<h2> On-line use</h2>
It is available to use online in the site: http://speech-tools.liaa.dc.uba.ar/coherence/


<h2> Install </h2>
The easy way to install is using pip, doing:

pip install git+https://github.com/facuzeta/coherence/

It takes some time becouse it has to download the trained models ( more than > 30 MB)

<h2> Example </h2>

After install...

```
import coherence

some_large_text= "The campaign brought ... I began by making up my mind..."

coh = coherence.coherenceAnalisys()
res = coh.analysis_text(some_large_text) 
```
*res* is the dictionary with the statistics, you can see the result using the on-line app http://speech-tools.liaa.dc.uba.ar/coherence/

<h2> How does it work? </h2>
<img src="https://images.nature.com/lw926/nature-assets/npjschz/2015/npjschz201530/images_hires/npjschz201530-f1.jpg" width=600px/>

<h2> Citation </h2>
Bedi G, Carrillo F, Cecchi GA, Slezak DF, Sigman M, Mota NB, Ribeiro S, Javitt DC, Copelli M, Corcoran CM. Automated analysis of free speech predicts psychosis onset in high-risk youths. npj Schizophrenia. 2015 Aug 26;1:15030.

