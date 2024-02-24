var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
        if(document.getElementById('quantite')){

            var quantite = document.getElementById('quantite').value; 
        }  

        else{quantite=1}
		var productId = this.dataset.product
		var action = this.dataset.action

		console.log('productId:', productId, 'Action:', action,"quantite:",quantite)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			console.log('not authentified')
            window.location.href = '/seconnecter';
    
		}else{
			updateUserOrder(productId, action,quantite)
		}
	})
}

function updateUserOrder(productId, action,quantite){
	console.log('User is authenticated, sending data...')

		var url = '/modifier_panier'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action,'quantite':quantite})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

