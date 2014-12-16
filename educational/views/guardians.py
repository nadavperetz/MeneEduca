from django.views.generic import DetailView
from educational.models import Assignment


class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'educational/guardian/assignment_detail.html'
