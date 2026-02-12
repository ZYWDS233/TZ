import re

# 读取wcp文件
with open('F:\\小蓝的冒险者指北\\TZ\\topics\\天舟.wcp', 'r', encoding='utf-8') as f:
    content = f.read()

# 解析TitleList
title_list = []
pattern = r'TitleList\.Title\.(\d+)=(.*?)\nTitleList\.Level\.(\d+)=(\d+)\nTitleList\.Url\.(\d+)=(.*?)\n'
title_matches = re.findall(pattern, content, re.DOTALL)

for match in title_matches:
    index = int(match[0])
    title = match[1]
    level = int(match[2])
    url = match[3]
    title_list.append({'index': index, 'title': title, 'level': level, 'url': url})

# 按index排序
title_list.sort(key=lambda x: x['index'])

# 生成HTML
html_content = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
<!-- saved from url=(0014)about:internet -->
<html>

<head>
	<title>天舟国度</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<style type="text/css">
		<!-- 
		.selected {
			font-weight: normal;
			background-color: #E2E2E2;
			padding: 0px, 2px, 0px, 2px;
		}

		.unselected {
			font-weight: normal;
			padding: 0px, 2px, 0px, 2px;
		}

		.hand {
			cursor: hand;
		}

		.p {
			height: 16px;
			width: 16px;
			vertical-align: middle;
			border: 0;
		}

		div,
		body {
			font-family: Tahoma, Verdana;
			font-size: 16px;
		}

		A:link {
			text-decoration: none;
			color: #000000
		}

		A:visited {
			text-decoration: none;
			color: #000000
		}

		A:active {
			text-decoration: none;
			color: #000000
		}

		A:hover {
			text-decoration: none;
			color: #FF0000
		}
		--> 
	</style>

	<SCRIPT LANGUAGE="JavaScript">
		<!--
		var cl,pn,pm,bl;
		var path = 'icons/';
		var pos = 0;
		var icon;
		var tar = 'content';
		var display;
		var imgi;
		var AutoCollapse;
		var LastSelected = -1;
		var loaded = false;
		var max;
		var divlist;
		
		function SetEnv(v,a){
		
		if(v==0){ 
			pn = [['daplus.gif','daminus.gif'],['tplus.gif','tminus.gif'],['uaplus.gif','uaminus.gif'],['splus.gif','sminus.gif']];
			PreloadImg('downangle.gif','tshaped.gif','upangle.gif','sline.gif','daplus.gif','daminus.gif','tplus.gif','tminus.gif','uaplus.gif','uaminus.gif','splus.gif','sminus.gif','blank.gif','line.gif');
		}else{
			pn = [['plus.gif','minus.gif']];
			PreloadImg('plus.gif','minus.gif','blank.gif');
		
		}
		AutoCollapse = a;
		}
		
		 function PreloadImg(){
		if (document.images) { 
			var imgs = PreloadImg.arguments; 
			var pload = new Array();
			for (var i=0; i<imgs.length; i++) { 
				pload[i] = new Image; 
				pload[i].src = path + imgs[i]; 
			} 
		} 
		 } 
		
		function get(o){
		var x;
		if(document.all) x=document.all[o]; 
		if(document.getElementById) x=document.getElementById(o);
		
		return x;
		}
		
		
		function pnImg(img){
		var i,j;
		for(i=0;i<=3;i++){
			for(j=0;j<=1;j++){
				if(img.substr(img.lastIndexOf('/') + 1)== pn[i][j]){
					return i;
				}
			}
		}
		}
		function icon(img){
		var f;
		f = img.substr(img.lastIndexOf('/') + 1);
		if( f=='1.gif' || f=='2.gif'){
			return ['1.gif','2.gif'];
		}
		if( f=='3.gif' || f=='4.gif'){
			return ['3.gif','4.gif'];
		}
		if( f=='5.gif' || f=='6.gif'){
			return ['5.gif','6.gif'];
		}
		if( f=='7.gif' || f=='8.gif'){
			return ['7.gif','8.gif'];
		}
		return [f,f];
		}
		
		function show(id){
		get('d' + id).style.display='block';
		if(get('imgn' + id )) get('imgn' + id ).src= path + pn[pnImg(get('imgn' + id ).src)][1];
		get('img' + id ).src= path + icon(get('img' + id ).src)[1];
		
		}
		
		function collapse(id){
		get('d' + id).style.display='none';
		if(get('imgn' + id )) get('imgn' + id ).src= path + pn[pnImg(get('imgn' + id ).src)][0];
		get('img' + id ).src= path + icon(get('img' + id ).src)[0];
		
		}
		
		function collapseAll(){
		var i;
		var o;
		for(i=0;i<=divlist.length-1;i++){
			if(o=get('d' + divlist[i])){
				if(o.style.display!='none'){ 
					collapse(divlist[i]);
				}
			}
		}
		}
		
		function showAll(){
		var i;
		var o;
		for(i=0;i<=divlist.length-1;i++){
			if(o=get('d' + divlist[i])){
				if(o.style.display!='block'){ 
					show(divlist[i]);
				}
			}
		}
		}
		
		function unselectAll(){
		var i=0;
		while(get("l" + i)){
			get("l" + i).className = "unselected";
			i++;
		}
		}
		
		function clickNode(index){
		var e;
		
		e = get("l" + index);
		if(e==null) return;
		e = e.parentNode;
		if(e.nodeName == 'A'){
			if(e.href!= window.location.href + '#'){
				parent.parent.content.location.href = e.href;
			}else{
				selectNode(index);
			}
			e.onclick;
		}
		}
		
		function showParent(ele){
		var e;
		e = ele.parentNode;
		
		if(e==null) return;
		
		if(e.nodeName == 'DIV'){
			if(e.id!='') show(e.id.substring(1,e.id.length ));
		}else if(e.nodeName == 'A'){
		
		}
		showParent(e);
		}
		
		function showNode(index){
		showParent(get("l" + index));
		LinkClick(index);
		}
		
		function selectNode(index){
		if(LastSelected!=index){
		//collapseAll();
		showParent(get("l" + index));
		LinkClick(index);
		get('l' + index).scrollIntoView(true);
		
		
		//alert(get('l' + index).offsetHeight + '|' + document.body.clientHeight + '|' + document.body.offsetHeight);
		window.scrollTo(0,document.body.scrollTop); // - document.body.clientHeight /3);
		}
		}
		
		
		function NodeClick(id){
		if(get('d' + id ).style.display=='none'){
			show(id);
		}else{
			collapse(id);
		}
		return false;
		}
		
		function LinkDblClick(id){
		if(!AutoCollapse){
			if(get('d' + id ).style.display=='none'){
				show(id);
			}else{
				collapse(id);
			}
		}
		return false;
		}
		
		function LinkClick(index,hasChild,r){
		if(AutoCollapse && hasChild){
			if(get('d' + index ).style.display=='none'){
				collapseAll()
				showParent(get('l' + index));
				show(index);
			}else{
				collapseAll()
				showParent(get('l' + index));
				collapse(index);
			}
		}
		if(LastSelected!=-1){
			get('l' + LastSelected).className = "unselected";
		}
		get('l' + index).className = "selected";
		LastSelected = index;
		return r;
		}
		
		/* function body_onmousemove(event){
		if(typeof(document.body.scrollTop)!='undefined'){
		if(parseInt(event.clientX)<5){
		window.scroll(0,document.body.scrollTop);}}
		if(typeof(window.scrollY)!='undefined'){
		if(parseInt(event.clientX)<5){
		window.scrollTo(0,window.scrollY);}}
		} */

		window.defaultStatus = '';

		function body_onload() {
			get('loading').style.display = 'none';
			loaded = true;
			if (parent.parent.content.document.readyState) {
				if (parent.parent.content.document.readyState == 'complete') {
					try { parent.parent.content.syn(); } catch (e) { };
				}
			} else {
				if (parent.parent.contentLoaded) {
					try { parent.parent.content.syn(); } catch (e) { };
				}
			}
		}

		//-->
	</SCRIPT>
	<script language="JavaScript" src="languages.js"></script>


</head>

<body bgcolor="#ffffff" leftmargin="5" topmargin="5" marginwidth="5" marginheight="5"
	onmousemove="body_onmousemove(event);" onload="body_onload();">
	<div id="loading">
		<font color="#FF0000" size="1"> Loading table of contents...
		</font><br><br>
	</div>
	<script>SetEnv(0,false)</script>
	
	<!-- 天舟国度目录结构 -->
'''

# 生成目录结构
level_stack = []
for item in title_list:
    index = item['index'] + 1  # HTML中从1开始
    title = item['title']
    level = item['level']
    url = item['url']
    
    # 处理层级
    while level_stack and level_stack[-1]['level'] >= level:
        level_stack.pop()
        html_content += '\t' * (len(level_stack) + 1) + '</div>\n'
    
    # 生成缩进
    indent = '\t' * (len(level_stack) + 1)
    
    # 检查是否有子节点
    has_child = False
    if title_list.index(item) < len(title_list) - 1:
        next_item = title_list[title_list.index(item) + 1]
        if next_item['level'] > level:
            has_child = True
    
    # 生成HTML
    if has_child:
        html_content += f'{indent}<div><nobr><a href="#" onClick="return NodeClick(\'{index}\')"><img id="imgn{index}" src="icons/tplus.gif" class="p"></a>'
    else:
        html_content += f'{indent}<div><nobr>'
    
    if url:
        html_content += f'<a href="topics/{url}" onclick="return LinkClick(\'{index}\',{str(has_child).lower()},true)" onDblClick="return LinkDblClick(\'{index}\')" target="content" title="{title}" onmousemove="window.status=\'{title}\';" class="hand"><img id="img{index}" src="icons/1.gif" class="p"> <span id="l{index}" class="unselected">{title}</span></a>'
    else:
        html_content += f'<a href="#" onclick="return LinkClick(\'{index}\',{str(has_child).lower()},true)" onDblClick="return LinkDblClick(\'{index}\')" target="content" title="{title}" onmousemove="window.status=\'{title}\';" class="hand"><img id="img{index}" src="icons/1.gif" class="p"> <span id="l{index}" class="unselected">{title}</span></a>'
    
    html_content += '</nobr></div>\n'
    
    # 生成子节点容器
    if has_child:
        html_content += f'{indent}<div id="d{index}" style="display:none">\n'
        level_stack.append({'level': level, 'index': index})

# 关闭所有未闭合的div
while level_stack:
    level_stack.pop()
    html_content += '\t' * (len(level_stack) + 1) + '</div>\n'

html_content += '''

</body>

</html>'''

# 写入文件
with open('F:\\小蓝的冒险者指北\\TZ\\webhelpcontents.htm', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('生成完成！')
