from rest_framework.pagination import CursorPagination

class MovieCursorPagination(CursorPagination):
    page_size = 5
    ordering = "-uploaded_at"
    cursor_query_param = "cursor"