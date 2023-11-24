const loading = document.getElementById('loading');
let data;

function clickTab(x) {
    let elem = document.getElementById("tab_" + x)
    if (elem.style.color === "rgb(18, 18, 18)")
        elem.style.color = "#056de8";
    for (let i = 0; i < 5; i++) {
        let temp = document.getElementById("tab_" + i)
        if (i !== x && temp.style.color === "rgb(5, 109, 232)")
            temp.style.color = "#121212";
    }
    loading.style.display = 'flex';
    getData(x).then((d) => {
        data = d;
        console.log(data);
        displayPage();
    });
}

async function getData(mode) {
    try {
        const response = await fetch('http://localhost:5000/api/data?mode=' + mode);
        const data = await response.json();
        // 使用返回的数据渲染页面
        loading.style.display = 'none';
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayPage() {
    if (data.length === 0) console.log("获取文章失败");
    const container = document.querySelector('.article-container');
    if (container) {
        container.innerHTML = '';
        getKeywordsWordcloud()
        // 遍历数据数组，渲染每个文章块
        for (let i = 0; i < data.authors.length; i++) {
            // 创建一个新的文章块元素
            let article = document.createElement('div');
            article.className = 'article';

            // 填充文章块的内容
            article.innerHTML = `
                <h2>${data.titles[i]}</h2>
                <p>Author: ${data.authors[i]}</p>
                <p>Keywords: ${data.keywords[i]}</p>
                <a href="${data.pdfs[i]}" target="_blank">Download PDF</a>
            `;

            // 将文章块添加到 article-container 中
            container.appendChild(article);
        }
    } else {
        console.error('Article container not found!');
    }
}

function initPage() {
    clickTab(0)
}

function getKeywordsWordcloud() {
    const container = document.querySelector('.img-container');
    container.innerHTML = '';
    fetch(`http://localhost:5000/api/keywords-wordcloud`)
        .then(response => response.blob())
        .then(blob => {
            // 创建一个表示图片的URL
            let imageUrl = URL.createObjectURL(blob);

            // 在页面上显示词云图片
            let imgElement = document.createElement('img');
            imgElement.src = imageUrl;
            container.appendChild(imgElement);
        })
        .catch(error => console.error('Error fetching wordcloud:', error));
}