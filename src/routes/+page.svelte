<script>
    let fileContent = '';
    let selectedDate = new Date().toISOString().split('T')[0];
    
    async function fetchFileContent(date) {
        try {
            const response = await fetch(`melon/${date}.melon`);
            if (response.status !== 200) {
                throw new Error('해당하는 날짜의 멜론차트 정보가 없습니다.');
            }
            fileContent = await response.text();
        } catch (error) {
            fileContent = `해당하는 날짜의 멜론차트 정보가 없습니다.`;
        }
    }

    function handleDateChange(event) {
        selectedDate = event.target.value;
        if (!selectedDate) {
            fileContent = '';
            return;
        }
        fetchFileContent(selectedDate);
    }
</script>

<svelte:head>
    <title>Home</title>
    <meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
    <div class="main-form">
        <input type="date" class="date-input" on:change="{handleDateChange}">
        <div class="file-content">
            {@html fileContent}
        </div>
    </div>
</section>

<style>
    .main-form {
        border: 3px solid #6ec953;
        border-radius: 0.5em;
        height: 35em;
        display: flex;
        align-items: center;
        flex-direction: column;
    }

    .date-input {
        background-color: #f0f0f0;
        border: 2px solid #6ec953;
        border-radius: 0.5em;
        padding: 0.5em;
        font-size: 1em;
        color: #333;
        cursor: pointer;
        width: 200px;
        transition: background-color 0.3s, border-color 0.3s;
        margin-top: 3em;
    }

    .date-input:focus {
        outline: none;
        background-color: #e0ffe0;
        border-color: #4caf50;
    }

    .file-content {
        margin-top: 1em;
        padding: 1em;
        border: 1px solid #ddd;
        border-radius: 0.5em;
        background-color: #f9f9f9;
        width: 100%;
        box-sizing: border-box;
        max-height: 1200px; 
        overflow-y: auto; 
        overflow-x: hidden;
    }
</style>
