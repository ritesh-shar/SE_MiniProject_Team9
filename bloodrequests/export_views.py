"""
Export views for donations and inventory in CSV and PDF formats.

# BBMS-F-052: Admins export donation and inventory reports as CSV and PDF,
#             matching on-screen data.
"""

import csv
import io
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework import status

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

from donations.models import Donation
from inventory.models import BloodStock


class CSVRenderer(BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class PDFRenderer(BaseRenderer):
    media_type = 'application/pdf'
    format = 'pdf'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


# BBMS-F-052
class DonationExportView(APIView):
    """
    Export all donation records as CSV or PDF.
    GET /api/requests/export/donations?format=csv|pdf
    """
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, CSVRenderer, PDFRenderer]

    def get(self, request):
        if request.user.role not in ('admin', 'staff'):
            return Response(
                {'error': 'Administrator access required.', 'code': 'FORBIDDEN'},
                status=status.HTTP_403_FORBIDDEN,
            )

        export_format = request.query_params.get('format', 'csv').lower()
        donations = Donation.objects.all().order_by('-donation_date', '-created_at')

        if export_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="donations_report.csv"'
            writer = csv.writer(response)
            writer.writerow(['ID', 'Donor Username', 'Blood Group', 'Component', 'Quantity (Units)', 'Donation Date', 'Created At'])

            for d in donations:
                writer.writerow([
                    d.id,
                    d.donor.username,
                    d.blood_group,
                    d.component,
                    d.quantity,
                    d.donation_date.isoformat(),
                    d.created_at.isoformat(),
                ])
            return response

        elif export_format == 'pdf':
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            elements.append(Paragraph("<b>Blood Bank Management System - Donations Report</b>", styles['Title']))
            elements.append(Spacer(1, 12))

            table_data = [['ID', 'Donor', 'Group', 'Component', 'Units', 'Date']]
            for d in donations:
                table_data.append([
                    str(d.id),
                    d.donor.username,
                    d.blood_group,
                    d.component,
                    str(d.quantity),
                    d.donation_date.isoformat(),
                ])

            t = Table(table_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#990000')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(t)
            doc.build(elements)

            pdf = buffer.getvalue()
            buffer.close()
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="donations_report.pdf"'
            response.write(pdf)
            return response

        return Response({'error': 'Unsupported format. Use ?format=csv or ?format=pdf'}, status=status.HTTP_400_BAD_REQUEST)


# BBMS-F-052
class InventoryExportView(APIView):
    """
    Export current inventory stock records as CSV or PDF.
    GET /api/requests/export/inventory?format=csv|pdf
    """
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, CSVRenderer, PDFRenderer]

    def get(self, request):
        if request.user.role not in ('admin', 'staff'):
            return Response(
                {'error': 'Administrator access required.', 'code': 'FORBIDDEN'},
                status=status.HTTP_403_FORBIDDEN,
            )

        export_format = request.query_params.get('format', 'csv').lower()
        stocks = BloodStock.objects.all().order_by('blood_group', 'component')

        if export_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'
            writer = csv.writer(response)
            writer.writerow(['Blood Group', 'Component', 'Units Available', 'Last Updated'])

            for s in stocks:
                writer.writerow([
                    s.blood_group,
                    s.component,
                    s.units_available,
                    s.last_updated.isoformat() if s.last_updated else '',
                ])
            return response

        elif export_format == 'pdf':
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            elements.append(Paragraph("<b>Blood Bank Management System - Inventory Stock Report</b>", styles['Title']))
            elements.append(Spacer(1, 12))

            table_data = [['Blood Group', 'Component', 'Units Available', 'Last Updated']]
            for s in stocks:
                table_data.append([
                    s.blood_group,
                    s.component,
                    str(s.units_available),
                    s.last_updated.strftime('%Y-%m-%d %H:%M') if s.last_updated else 'N/A',
                ])

            t = Table(table_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(t)
            doc.build(elements)

            pdf = buffer.getvalue()
            buffer.close()
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'
            response.write(pdf)
            return response

        return Response({'error': 'Unsupported format. Use ?format=csv or ?format=pdf'}, status=status.HTTP_400_BAD_REQUEST)
