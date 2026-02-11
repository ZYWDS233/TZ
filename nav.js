// 导航栏HTML
const navHtml = `
<h3>天舟导航</h3>
<ul>
    <li><a href="01 天舟国度\01 天舟国度.html" target="_top">01 天舟国度</a>
        <ul>
            <li><a href="01 天舟国度\01 宇宙的中心：天舟星\宇宙的中心：天舟星.html" target="_top">宇宙的中心：天舟星</a>
                <ul>
                    <li><a href="01 天舟国度\01 宇宙的中心：天舟星\历法.html" target="_top">历法</a></li>
                    <li><a href="01 天舟国度\01 宇宙的中心：天舟星\天舟星地图\天舟星地图.htm" target="_top">天舟星地图</a>
                        <ul>
                            <li><a href="01 天舟国度\01 宇宙的中心：天舟星\天舟星地图\西洲国家和地区\西洲国家和地区.html" target="_top">西洲国家和地区</a></li>
                            <li><a href="01 天舟国度\01 宇宙的中心：天舟星\天舟星地图\东洲的国家和地区\东洲的国家和地区.html" target="_top">东洲的国家和地区</a></li>
                        </ul>
                    </li>
                    <li><a href="01 天舟国度\01 宇宙的中心：天舟星\经济.html" target="_top">经济</a></li>
                    <li><a href="01 天舟国度\01 宇宙的中心：天舟星\语言.html" target="_top">语言</a></li>
                </ul>
            </li>
            <li><a href="01 天舟国度\03 天舟国度的诸神\天舟国度的诸神.html" target="_top">天舟国度的诸神</a></li>
            <li><a href="01 天舟国度\02 天舟国度的位面学.html" target="_top">天舟国度的位面学</a></li>
        </ul>
    </li>
    <li><a href="02 新的冒险\02 新的冒险.html" target="_top">02 新的冒险</a>
        <ul>
            <li><a href="02 新的冒险\01 种族\种族.html" target="_top">01 种族</a></li>
            <li><a href="02 新的冒险\02 职业\02 职业.html" target="_top">02 职业</a></li>
        </ul>
    </li>
</ul>
`;

// 导航栏样式
const navStyles = `
<style>
    /* 导航栏样式 */
    .sidebar {
        width: 270px;
        position: fixed;
        left: 0;
        top: 0;
        bottom: 0;
        background: #f0f0f0;
        padding: 20px;
        overflow-y: auto;
        font-family: Arial, DengXian, Microsoft YaHei, sans-serif;
    }
    
    .sidebar h3 {
        margin-top: 0;
        color: #333;
        border-bottom: 2px solid #ddd;
        padding-bottom: 10px;
    }
    
    .sidebar ul {
        list-style: none;
        padding-left: 0;
        margin: 0;
    }
    
    .sidebar ul ul {
        padding-left: 20px;
    }
    
    .sidebar li {
        margin: 5px 0;
    }
    
    .sidebar a {
        color: #333;
        text-decoration: none;
        display: block;
        padding: 5px 10px;
        border-radius: 4px;
        transition: background-color 0.2s;
    }
    
    .sidebar a:hover {
        background-color: #e0e0e0;
    }
    
    /* 内容区域样式 */
    .content {
        margin-left: 290px;
        padding: 20px;
        font-family: Arial, DengXian, Microsoft YaHei, sans-serif;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .sidebar {
            width: 100%;
            position: relative;
            height: auto;
            max-height: 300px;
        }
        .content {
            margin-left: 0;
        }
    }
</style>
`;

// 加载导航栏
function loadNavigation() {
    // 添加样式
    document.head.insertAdjacentHTML('beforeend', navStyles);
    
    // 创建导航栏容器
    const navContainer = document.createElement('div');
    navContainer.className = 'sidebar';
    navContainer.innerHTML = navHtml;
    
    // 将导航栏添加到页面顶部
    document.body.insertAdjacentElement('afterbegin', navContainer);
    
    // 调整内容区域位置
    document.body.style.margin = '0';
    
    // 创建内容容器
    const contentContainer = document.createElement('div');
    contentContainer.className = 'content';
    
    // 移动现有内容到内容容器
    while (document.body.children.length > 1) {
        if (document.body.children[1].className !== 'sidebar') {
            contentContainer.appendChild(document.body.children[1]);
        } else {
            break;
        }
    }
    
    // 添加内容容器到页面
    document.body.appendChild(contentContainer);
}

// 页面加载完成后加载导航栏
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadNavigation);
} else {
    loadNavigation();
}
