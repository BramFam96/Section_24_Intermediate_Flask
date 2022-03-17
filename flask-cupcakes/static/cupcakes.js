URL = 'http://localhost:5000/api'

// html structure for individual cupcakes
function makeCupcakeHTML(cupcake) {
	return `
    <div data-cupcake-id=${cupcake.id} class= text-center>
    <img class="Cupcake-img"
            src="${cupcake.image}"
            alt="default image of chocolate cupcake">
      <p>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating} &star;
      </p>
      <button class="btn btn-danger delete-button">Delete</button>
    </div>
  `
}

// fetch and display cupcake list
async function fetchCupcakes() {
	const res = await axios.get(`${URL}/cupcakes`)
	for (let cupcake of res.data.cupcakes) {
		let $newCupcake = $(makeCupcakeHTML(cupcake))
		$newCupcake.appendTo('#cupcake-list')
	}
}

// create and append submission handler to submit button
$('#new-cupcake-form').on('submit', async function (e) {
	e.preventDefault()
	let flavor = $('#form-flavor').val()
	let rating = $('#form-rating').val()
	let size = $('#form-size').val()
	let image = $('#form-image').val()

	const res = await axios.post(`${URL}/cupcakes`, {
		flavor,
		rating,
		size,
		image,
	})

	let cupcake = $(makeCupcakeHTML(res.data.cupcake))
	cupcake.appendTo('#cupcake-list')
	$('#new-cupcake-form').trigger('reset')
})


// create and append delete handler to delete button
$('#cupcake-list').on('click', '.delete-button', async function (e) {
	e.preventDefault()
	let $cupcake = $(e.target).closest('div')
	let id = $cupcake.attr('data-cupcake-id')
	await axios.delete(`${URL}/cupcakes/${id}`)
	$cupcake.remove()
})

$(fetchCupcakes)

