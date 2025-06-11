let messages = fetch('http://127.0.0.1:5000/api/sms')
    .then( response => response.json())
    .then( data => {
        const container = document.getElementById('sms-container')
        data.forEach(sms => {
            const card = document.createElement('div');
            card.classList.add('sms-card');

            card.innerHTML = `
                ${sms.type && `<h3>${sms.type}</h3>`}
                ${sms.sender && `<p><strong>Sender:</strong> ${sms.sender}</p>`}
                ${sms.amount != null && `<p><strong>Amount:</strong> ${sms.amount} RWF</p>`}
                ${sms.time && `<p><strong>Time:</strong> ${sms.time}</p>`}
                ${sms.message && `<p><strong>Message:</strong> ${sms.message}</p>`}
                ${sms.new_balance != null && `<p><strong>New Balance:</strong> ${sms.new_balance} RWF</p>`}
            `;

            container.appendChild(card);
        });
    })
    .catch(err => console.error('Error fetching SMS:', err))