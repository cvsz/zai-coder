from zai_coder.quality_assurance_test_lab.routes import (
    route_qa_page, route_qa_matrix_page, route_qa_regression_page,
    route_qa_fixtures_page, route_qa_gates_page,
)
render_qa_overview_page = lambda: route_qa_page()["html"]
render_matrix_page = lambda: route_qa_matrix_page()["html"]
render_regression_page = lambda: route_qa_regression_page()["html"]
render_fixtures_page = lambda: route_qa_fixtures_page()["html"]
render_gates_page = lambda: route_qa_gates_page()["html"]
