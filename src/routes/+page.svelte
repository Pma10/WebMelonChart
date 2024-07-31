<script>
    let fileContent = '';
    let selectedDate = new Date().toISOString().split('T')[0];
    let dateOptions = [
		'2024-07-31'
	];


    async function fetchFileContent(date) {
        try {
            const response = await fetch(`melon/${date}.pm`);
            if (response.status !== 200) {
                throw new Error('파일을 찾을 수 없습니다.');
            }
            fileContent = await response.text();
        } catch (error) {
            fileContent = `에러발생: ${error.message}`;
        }
    }

    function handleSelectChange(event) {
        selectedDate = event.target.value;
        if (selectedDate === 'none') {
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
        <select name="date" class="sel-form" on:change="{handleSelectChange}">
            <option value="none">선택하기</option>
            {#each dateOptions as date}
                <option value="{date}">{date}</option>
            {/each}
        </select>
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

    .sel-form {
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

    .sel-form:focus {
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
