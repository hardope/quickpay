const topUpButton = document.getElementById('topUpButton');
const popupForm = document.getElementById('popupForm');
var userdata;

topUpButton.addEventListener('click', function() {
    popupForm.classList.add('active');
});

popupForm.addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Get the form input values
    const cardNumber = document.querySelector('input[placeholder="Card Number"]').value;
    const expiryDate = document.querySelector('input[placeholder="Expiry Date"]').value;
    const cvv = document.querySelector('input[placeholder="CVV"]').value;

    // Perform basic validation (you can add more robust validation as needed)
    if (cardNumber.trim() === '' || expiryDate.trim() === '' || cvv.trim() === '') {
        alert('Please fill in all fields.');
        return;
    }

    // Simulate payment processing (you can replace this with actual payment processing logic)
    setTimeout(function() {
        alert('Payment successful! Thank you for your purchase.');
        popupForm.classList.remove('active');
    }, 2000); // Simulating a 2-second payment processing delay
});


const host = "http://localhost:8000";
const dom = document

document.addEventListener('DOMContentLoaded', function() {

    mytoken = localStorage.getItem('quickpay-token');

    document.getElementById('receiver-no').addEventListener('keyup', function() {

        let value = dom.getElementById('receiver-no').value

        if (value.length == 10) {

            let request = new XMLHttpRequest();
            request.open('GET', host + '/account/get-user-acc/' + value, true);
            request.setRequestHeader('Content-Type', 'application/json');
            request.setRequestHeader('Authorization', 'Bearer ' + mytoken);
            
            request.onload = function() {
                if (request.status == 200) {
                    user = JSON.parse(request.response)['data']
                    dom.getElementById('name').value = `${user['username']} - ${user['first_name']} ${user['last_name']}`
                } else {
                    alert('Invalid Account Number')
                    dom.getElementById('name').value = ""
                    console.error('Error fetching account information:', request.status);
                }
            };
            
            request.send();
        }
    });
    

    if (mytoken) {
        fetch(host + "/account/get-me", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + mytoken
            }
        })
        .then(response => response.json())
        .then(data => {

            if (data['detail'] == "Given token not valid for any token type") {
                window.location.href = "index.html"
            }

            if (data['data']['username']) {
                dom.getElementById('username').innerHTML = data['data']['username']
                dom.getElementById('balance').innerHTML = `$ ${data['data']['wallet_balance']}`
                dom.getElementById('acc-no').innerHTML = `Acc No - ${data['data']['acc_no']}`
            } else {
                window.location.href = "index.html"
            }
        });
    }

    fetch(host + '/account/view-transactions', {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + mytoken
        },
    })
    .then(response => response.json())
    .then(data => {
        let transactions = data['transactions']
        if (data['status'] == false) {
            dom.getElementById('table-body').append('Your Recent Transactions will appear here')
        } else {
            for (let i = 0; i < transactions.length; i++) {

                if (i > 7) {
                    break
                }

                let sender = transactions[i]['sender'];
                let receiver = transactions[i]['receiver'];
                let created_at = transactions[i]['created_at'];
                let amount = transactions[i]['amount'];
            
                if (sender == dom.getElementById('username').innerHTML) {
                    dom.getElementById('table-body').innerHTML += `
                        <tr>
                            <td>${receiver}</td>
                            <td>${created_at}</td>
                            <td>-$${amount}</td>
                        </tr>
                    `
                } else {
                    dom.getElementById('table-body').innerHTML += `
                        <tr>
                            <td>${receiver}</td>
                            <td>${created_at}</td>
                            <td>$${amount}</td>
                        </tr>
                    `
                }
            }
        }
    })
});

function transfer() {

    const host = "http://localhost:8000";
    const acc_no = dom.getElementById('receiver-no').value
    const amount = dom.getElementById('amount').value;
    const pin = dom.getElementById('pin').value;

    let request = new XMLHttpRequest();
    request.open('POST', host + '/account/transfer', true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('Authorization', 'Bearer ' + mytoken);
    request.send(JSON.stringify({
        "acc": acc_no,
        "amount": amount,
        "pin": pin
    }));

    request.onload = function() {
        if (request.status === 200) {
            // Reset the form
            document.getElementById("reciever-no").value = ""
            document.getElementById("pin").value = ""
            document.getElementById("amount").value = ""
            window.location.href = window.location.href +  `?` 
        } else {
            let data = JSON.parse(request.response);
            alert(data.message);
        }
    };
}