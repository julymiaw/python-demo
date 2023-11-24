const loading = document.getElementById('loading');

function initPage(){
    getData();
}

function clickTab(x) {
    let elem = document.getElementById("tab_"+x)
    if(elem.style.color==="rgb(18, 18, 18)")
        elem.style.color="#056de8";
    for(let i=0;i<5;i++){
        let temp = document.getElementById("tab_"+i)
        if(i!=x && temp.style.color==="rgb(5, 109, 232)")
            temp.style.color="#121212";
    }
}

async function getData() {
    const mode = 0;
    try {
        const response = await fetch('http://localhost:5000/api/data?mode=' + mode);
        const data = await response.json();
        // 使用返回的数据渲染页面
        console.log(data);
        loading.style.display = 'none';
    } catch (error) {
        console.error('Error:', error);
    }
}
