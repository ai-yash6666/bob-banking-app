from flask import render_template_string

_BASE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>{title}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
        integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
        crossorigin="anonymous"/>
</head>
<body class="bg-light">
  <div class="container mt-5 text-center">
    <h1 class="display-1 text-muted">{code}</h1>
    <h2 class="mb-3">{heading}</h2>
    <p class="text-muted">{message}</p>
    <a href="/" class="btn btn-primary mt-3">Go to Login</a>
  </div>
</body>
</html>
"""


def register_error_handlers(app):
    """Attach custom error pages for 404 and 500 responses."""

    @app.errorhandler(404)
    def not_found(e):
        html = _BASE.format(
            title="404 — Page Not Found",
            code="404",
            heading="Page Not Found",
            message="The page you are looking for does not exist.",
        )
        return render_template_string(html), 404

    @app.errorhandler(500)
    def internal_error(e):
        html = _BASE.format(
            title="500 — Server Error",
            code="500",
            heading="Something Went Wrong",
            message="An unexpected error occurred. Please try again later.",
        )
        return render_template_string(html), 500
