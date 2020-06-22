let btns=document.getElementsByClassName("addcart")
for(var i=0;i<btns.length;i++){
    btns[i].addEventListener('click',function(){
        productId=this.dataset.product
        action=this.dataset.action
        console.log(productId,action)
         
        if(user=='AnonymousUser'){
            console.log('Not logged in')
        }
        else{
            updateUserOrder(productId,action)
        }

    })
}

function updateUserOrder(productId,action){
    console.log("user sending data..")
    var url='/update_item/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then((response) =>{
        return response.json();
    })

    .then((data) =>{
        console.log('data:',data)
        location.reload()
    });
}