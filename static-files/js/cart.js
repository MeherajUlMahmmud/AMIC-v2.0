var updateBtns = document.getElementsByClassName("update-cart");

for (let i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener("click", function () {
		var medicineID = this.dataset.food;
		var action = this.dataset.action;
		console.log("medicineID: ", medicineID, "action: ", action);

		updateCart(medicineID, action);
	});
}

function updateCart(medicineID, action) {
	console.log("User logged in");

	var url = "cart/update-item/";

	fetch(url, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrftoken,
		},
		body: JSON.stringify({ medicineID: medicineID, action: action }),
	})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			console.log("data:", data);
			location.reload();
		});
}
