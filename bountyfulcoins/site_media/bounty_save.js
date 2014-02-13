fucntion bounty_save() {
	var item = $(this).parent();
	var data = {
		url: item.find("#id_url").val(),
		title: item.find("#id_title").val(),
		amount: item.find("#id_amount").val(),
		currency: item.find("#id_currency").val(),
		description: item.find("#id_description").val(),
		tags: item.find("#id_tags").val()
	};
	$.post("/save/?ajax", data, function (result) {
		if (result != "failure") {
			item.before($("li", resut).get(0));
			item.remove();
			$("ul.bounties .edit").click(bounty_edit);
		}
		else {
			alert("Failed to validate the bounty details before saving.");
		}
	});
	return false;