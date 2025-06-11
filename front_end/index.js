let messages = fetch('http://127.0.0.1:5000/api/sms')
    .then( response => response.json())
    .then( data => {
        const container = document.getElementById('sms-container')
        data.forEach(sms => {
            const card = document.createElement('div');
            card.classList.add('sms-card');

            card.innerHTML = `
                <div class='info-container'>
                ${sms.type  ? `<h3>${sms.type}</h3>` : ''}
                ${sms.sender  ? `<p><strong>Sender:</strong> ${sms.sender}</p>` : ''}
                ${sms.receiver  ? `<p><strong>receiver:</strong> ${sms.receiver}</p>` : ''}
                ${sms.amount  ? `<p><strong>Amount:</strong> ${sms.amount} RWF</p>` : ''}
                ${sms.new_balance != null ? `<p><strong>New Balance:</strong> ${sms.new_balance} RWF</p>` : ''}
                ${sms.time != null ? `<p><strong>Time:</strong> ${sms.time}</p>` : ''}
                </div>
                ${sms.message ? `<div class='message-container hidden'><strong>Message:</strong> ${sms.message}</div>` : ''}
                <button class='show-btn btn'>Show SMS</button>
                <button class='hide-btn btn hidden'>Hide SMS</button>
            `;
            const message_container = card.querySelector('.message-container')
            const show_sms_btn = card.querySelector('.show-btn')
            const hide_sms_btn = card.querySelector('.hide-btn')
            show_sms_btn.addEventListener('click', () => {
                message_container.classList.remove('hidden')
                show_sms_btn.classList.add('hidden')
                hide_sms_btn.classList.remove('hidden')
            })
            hide_sms_btn.addEventListener('click', () => {
                message_container.classList.add('hidden')
                show_sms_btn.classList.remove('hidden')
                hide_sms_btn.classList.add('hidden')
            })
            container.appendChild(card);
        });
    })
    .catch(err => console.error('Error fetching SMS:', err))