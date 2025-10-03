const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// API: 获取图数据
app.get('/api/graph', (req, res) => {
    try {
        const dataPath = path.join(__dirname, 'viz_data', 'graph.json');
        const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: '数据加载失败', message: error.message });
    }
});

// API: 获取统计信息
app.get('/api/stats', (req, res) => {
    try {
        const dataPath = path.join(__dirname, 'viz_data', 'graph.json');
        const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

        // 计算统计
        const stats = {
            nodes: data.nodes.length,
            edges: data.edges.length,
            types: [...new Set(data.nodes.map(n => n.tag))].length
        };

        res.json(stats);
    } catch (error) {
        res.status(500).json({ error: '统计计算失败' });
    }
});

// 主页
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 启动服务器
app.listen(PORT, () => {
    console.log(`\n🚀 GraphRAG 可视化服务器启动成功！`);
    console.log(`📊 访问: http://localhost:${PORT}`);
    console.log(`🎨 使用 Sigma.js 渲染知识图谱\n`);
});
