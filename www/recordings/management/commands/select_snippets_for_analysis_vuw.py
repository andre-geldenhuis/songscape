import random
import shutil

from django.core.management.base import BaseCommand, CommandError

from www.recordings.models import Snippet, Analysis, AnalysisSet, Detector, Score, Deployment

class Command(BaseCommand):
    def handle(self, *args, **options):
        analysis = Analysis.objects.get(code='hihi_id')
        deployments = Deployment.objects.all()
        clipping = Detector.objects.get(code='amplitude')
        code = 'simple-north-island-brown-kiwi'
        version = '0.1.2'
        detector = Detector.objects.get(code=code, version=version)
        for deployment in deployments:
            # get unclipped_snippets
            snippets = Snippet.objects.\
                filter(recording__deployment=deployment).\
                filter(scores__detector = detector, scores__score__lt = 1e10).\
                filter(scores__detector = \
                    Detector.objects.get(code='amplitude'), scores__score__lt=32000)
            n_snippets = snippets.count()
            random_already = snippets.filter(sets__analysis=analysis,
                sets__selection_method=u'Randomly selected 2%')
            kiwi_already = snippets.filter(sets__analysis=analysis,
                sets__selection_method=u'Simple NIBK score higher than 25 ')
            already = snippets.filter(sets__analysis=analysis)
            snippets = Snippet.objects.all()
            n_snippets = snippets.count()
            #select by kiwi score
            kiwi_snippets = snippets.filter(scores__detector=detector,
                scores__score__gt=25).exclude(id__in=already)
            #Now select a random 2%
            random_snippets = []
            if len(random_already) < round(0.02*n_snippets):
                random_snippets = list(snippets.\
                    exclude(id__in=already).\
                    exclude(id__in=kiwi_snippets).\
                    order_by('?')[:(round(n_snippets*0.02) - len(random_already))])

            snippet_set = zip(random_snippets, ['Randomly selected 2%']*len(random_snippets)) +\
                zip(list(kiwi_snippets), ['Simple NIBK score higher than 25 ']*len(kiwi_snippets))
            random.shuffle(snippet_set)

            print deployment, n_snippets, len(already), len(kiwi_snippets), len(random_snippets)
            for snip, reason in snippet_set:
                AnalysisSet(analysis=analysis, snippet=snip, selection_method=reason).save()
