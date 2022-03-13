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
// $('#new-cupcake-form').on('submit', async function (evt) {
// 	evt.preventDefault()

// 	let flavor = $('#form-flavor').val()
// 	let rating = $('#form-rating').val()
// 	let size = $('#form-size').val()
// 	let image = $('#form-image').val()

// 	const res = await axios.post(`${BASE_URL}/cupcakes`, {
// 		flavor,
// 		rating,
// 		size,
// 		image,
// 	})

// 	let $newCupcake = $(generateCupcakeHTML(res.data.cupcake))
// 	$newCupcake.appendTo('#cupcake-list')
// 	$('#new-cupcake-form').trigger('reset')
// })
// handle deleting cupcake

// create and append delete handler to delete button
$('#cupcake-list').on('click', '.delete-button', async function (e) {
	e.preventDefault()
	let $cupcake = $(e.target).closest('div')
	let id = $cupcake.attr('data-cupcake-id')
	await axios.delete(`${URL}/cupcakes/${id}`)
	$cupcake.remove()
})

$(fetchCupcakes)

// /** given data about a cupcake, generate html */

// function generateCupcakeHTML(cupcake) {
// 	return `
//     <div data-cupcake-id=${cupcake.id}>
//     <img style = "width:150px; height: 150px;" class="Cupcake-img"
//             src="${cupcake.image}"
//             alt="(no image provided)">
//       <p>
//         ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating} &star;

//       </p>
//       <button class="delete-button">X</button>
//     </div>
//   `
// }

// /** put initial cupcakes on page. */

// async function showInitialCupcakes() {
// 	const response = await axios.get(`${BASE_URL}/cupcakes`)

// 	for (let cupcakeData of response.data.cupcakes) {
// 		console.log(cupcakeData)
// 		let $newCupcake = $(generateCupcakeHTML(cupcakeData))
// 		$newCupcake.appendTo('#cupcake-list')
// 	}
// }

// /** handle form for adding of new cupcakes */

// $('#new-cupcake-form').on('submit', async function (evt) {
// 	evt.preventDefault()

// 	let flavor = $('#form-flavor').val()
// 	let rating = $('#form-rating').val()
// 	let size = $('#form-size').val()
// 	let image = $('#form-image').val()

// 	const res = await axios.post(`${BASE_URL}/cupcakes`, {
// 		flavor,
// 		rating,
// 		size,
// 		image,
// 	})

// 	let $newCupcake = $(generateCupcakeHTML(res.data.cupcake))
// 	$newCupcake.appendTo('#cupcake-list')
// 	$('#new-cupcake-form').trigger('reset')
// })

// /** handle clicking delete: delete cupcake */

// $('#cupcakes-list').on('click', '.delete-button', async function (evt) {
// 	evt.preventDefault()
// 	let $cupcake = $(evt.target).closest('div')
// 	let cupcakeId = $cupcake.attr('data-cupcake-id')

// 	await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`)
// 	$cupcake.remove()
// })

// $(showInitialCupcakes)
