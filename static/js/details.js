document.addEventListener('DOMContentLoaded', () => {
    const statusSelect = document.getElementById('status-select');
    const badgeStatus = document.getElementById('current-status');
    const textStatus = document.getElementById('text-status');

    if (statusSelect) {
        statusSelect.addEventListener('change', async (e) => {
            const newStatus = e.target.value;
            const studentId = statusSelect.getAttribute('data-id');

            try {
                const response = await fetch(`/api/students/${studentId}/status`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ status: newStatus })
                });

                const data = await response.json();

                if (data.success) {
                    badgeStatus.textContent = data.status;
                    textStatus.textContent = data.status;
                } else {
                    alert('Failed to update status');
                }
            } catch (error) {
                console.error('Error updating status:', error);
                alert('An error occurred.');
            }
        });
    }
});
