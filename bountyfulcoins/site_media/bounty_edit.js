function bounty_edit() {
	var item = $(this).parent();
	var url = item.find(".title").attr("href");
	item.load(
		"/save/?ajax&url=" + encodeURIComponent(url,
			null,
			function () {
				$("#save-form").submit(bounty_save);
			}
		);
		return false;
}

$(document).ready(function () {
	$("ul.bounties .edit").click(bounty_edit);
});