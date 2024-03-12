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
    const acc_no = dom.getElementById('acc-no').innerHTML
    const amount = dom.getElementById('amount').value;

    console.log(acc_no, amount, mytoken);

    let request = new XMLHttpRequest();
    request.open('POST', host + '/account/transfer', true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('Authorization', 'Bearer ' + mytoken);
    request.send(JSON.stringify({
        "acc": acc_no,
        "amount": amount
    }));

    request.DONE = function() {
        if (request.status == 200) {
            alert('Transfer Successful');
            window.location.href = "dashboard.html";
        } else {
            console.log(request.response);
            alert('Transfer Failed');
        }
    }
}