let allMessages = []

// Call the fetchMessages once the DOM has fully loaded
document.addEventListener('DOMContentLoaded', () => {
  fetchMessages();
  document.getElementById('search-btn').addEventListener('click', handleSearch);
  document.getElementById('filter-btn').addEventListener('click', applyFilters);
})

// Fetch SMS from the API endpoint.
function fetchMessages() {
  fetch('http://127.0.0.1:5000/api/sms')
    .then(response => response.json())
    .then(data => {
      allMessages = data;
      renderMessages(allMessages);
    })
    .catch(err => console.error('Error fetching SMS:', err));
}

// Render the SMS to the DOM.
function renderMessages(messages) {
    const container = document.getElementById('sms-container')
    const summaryContainer = document.getElementById('summary')
    container.innerHTML = ''
    if (messages.length === allMessages.length) {
        summaryContainer.textContent = `Showing all ${allMessages.length} SMS messages — no filter applied`;;
    } else {
        summaryContainer.textContent = `Showing ${messages.length} SMS messages matching your filters out of ${allMessages.length} total`;
    }
    messages.forEach(sms => {
        const card = document.createElement('div')
        card.classList.add('sms-card')

        card.innerHTML = `
            <div class='info-container'>
            ${sms.type  ? `<h3 class='large'>${sms.type}</h3>` : ''}
            ${sms.sender  ? `<p><strong>Sender:</strong> ${sms.sender}</p>` : ''}
            ${sms.receiver  ? `<p><strong>receiver:</strong> ${sms.receiver}</p>` : ''}
            ${sms.amount  ? `<p><strong>Amount:</strong> ${sms.amount} RWF</p>` : ''}
            ${sms.new_balance != null ? `<p><strong>New Balance:</strong> ${sms.new_balance} RWF</p>` : ''}
            ${sms.time != null ? `<p><strong>Time:</strong> ${sms.time}</p>` : ''}
            </div>
            ${sms.message ? `<div class='message-container hidden large'><strong>Message:</strong> ${sms.message}</div>` : ''}
            <button class='show-btn btn'>Show SMS</button>
            <button class='hide-btn btn hidden'>Hide SMS</button>
        `;
        const message_container = card.querySelector('.message-container')
        const show_sms_btn = card.querySelector('.show-btn')
        const hide_sms_btn = card.querySelector('.hide-btn')

        // Toggle functionality to show the message on the card.
        show_sms_btn.addEventListener('click', () => {
            message_container.classList.remove('hidden')
            show_sms_btn.classList.add('hidden')
            hide_sms_btn.classList.remove('hidden')
        })
        // Toggle functionality to hide the message on the card.
        hide_sms_btn.addEventListener('click', () => {
            message_container.classList.add('hidden')
            show_sms_btn.classList.remove('hidden')
            hide_sms_btn.classList.add('hidden')
        })

        container.appendChild(card);
    });
}

// Handle search functionality by filtering messages based on search input.
function handleSearch() {
    document.getElementById('type-filter').value = '';
    document.getElementById('min-amount').value = '';
    document.getElementById('max-amount').value = '';
    document.getElementById('date-filter').value = '';
    const searchInputElement = document.getElementById('search-input')
    
    if (!searchInputElement) {
        console.error('Search input element not found')
        return
    }
    
    const searchInput = searchInputElement.value.toLowerCase().trim()
    
    if (!searchInput) {
        renderMessages(allMessages)
        return
    }
    
    const filtered_sms = allMessages.filter(sms =>
        sms.message && sms.message.toLowerCase().includes(searchInput)
    )
    renderMessages(filtered_sms)
    searchInputElement.value = ''
}

// Apply multiple filters based on filters' inputs.
function applyFilters() {
    const type = document.getElementById('type-filter').value
    const minAmount = parseInt(document.getElementById('min-amount').value)
    const maxAmount = parseInt(document.getElementById('max-amount').value)
    const date = document.getElementById('date-filter').value

    const filtered = allMessages.filter(sms => {
        const matchesType = !type || sms.type === type
        const matchesMin = !minAmount || (sms.amount != null && sms.amount >= minAmount)
        const matchesMax = !maxAmount || (sms.amount != null && sms.amount <= maxAmount)
        const matchesDate = !date || (sms.time && sms.time.startsWith(date))
        return matchesType && matchesMin && matchesMax && matchesDate
    })

  renderMessages(filtered)
}




