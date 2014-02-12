function search_submit() {
	var query = $("#id_query").val();
	$("#search_results").load(
	"/search/?ajax&query=" + encodeURIComponent(query)
	):
	return false;
}