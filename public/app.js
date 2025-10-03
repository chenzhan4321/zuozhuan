// GraphRAG 知识图谱可视化

class GraphViz {
    constructor() {
        this.graph = null;
        this.renderer = null;
        this.data = null;
        this.typeColors = {
            'PERSON': '#e91e63',
            'ORGANIZATION': '#9c27b0',
            'GEO': '#4caf50',
            'EVENT': '#ff9800',
            'UNKNOWN': '#757575'
        };

        this.init();
    }

    async init() {
        console.log('🚀 初始化...');

        try {
            await this.loadData();
            this.createGraph();
            this.createRenderer();
            this.setupEvents();
            this.createLegend();
            this.createClusters();

            document.getElementById('loading').style.display = 'none';
            console.log('✅ 完成');
        } catch (error) {
            console.error('❌ 错误:', error);
            this.showError(error.message);
        }
    }

    async loadData() {
        console.log('📊 加载数据...');

        const [graphRes, statsRes] = await Promise.all([
            fetch('/api/graph'),
            fetch('/api/stats')
        ]);

        this.data = await graphRes.json();
        const stats = await statsRes.json();

        document.getElementById('nodeCount').textContent = stats.nodes;
        document.getElementById('edgeCount').textContent = stats.edges;

        console.log(`✓ ${stats.nodes} 节点, ${stats.edges} 边`);
    }

    createGraph() {
        console.log('🎨 创建图...');

        this.graph = new graphology.Graph();

        // 添加节点
        this.data.nodes.forEach((node, i) => {
            const angle = (i / this.data.nodes.length) * Math.PI * 2;
            const radius = 400;

            this.graph.addNode(node.key, {
                label: node.label,
                size: Math.log(node.degree + 2) * 4,
                color: this.typeColors[node.tag] || this.typeColors['UNKNOWN'],
                x: Math.cos(angle) * radius,
                y: Math.sin(angle) * radius,
                tag: node.tag,
                description: node.description,
                degree: node.degree
            });
        });

        // 添加边
        this.data.edges.forEach(edge => {
            if (this.graph.hasNode(edge.source) && this.graph.hasNode(edge.target)) {
                try {
                    this.graph.addEdge(edge.source, edge.target, {
                        size: 1,
                        color: '#e0e0e0',
                        label: edge.label
                    });
                } catch (e) {}
            }
        });

        // 应用布局
        if (typeof forceAtlas2 !== 'undefined') {
            forceAtlas2.assign(this.graph, {
                iterations: 50,
                settings: {
                    gravity: 1,
                    scalingRatio: 10,
                    slowDown: 3
                }
            });
        }

        console.log(`✓ ${this.graph.order} 节点, ${this.graph.size} 边`);
    }

    createRenderer() {
        console.log('🖼️ 创建渲染器...');

        const container = document.getElementById('container');

        this.renderer = new Sigma(this.graph, container, {
            renderLabels: true,
            labelSize: 12,
            labelWeight: '500',
            labelColor: { color: '#333' },
            defaultEdgeColor: '#e0e0e0',
            labelRenderedSizeThreshold: 2
        });

        console.log('✓ 渲染器创建完成');
    }

    setupEvents() {
        // Sigma 事件
        this.renderer.on('clickNode', ({ node }) => {
            this.showNodeDetails(node);
        });

        this.renderer.on('enterNode', ({ node }) => {
            const attrs = this.graph.getNodeAttributes(node);
            this.graph.setNodeAttribute(node, 'highlighted', true);
            this.renderer.refresh();
        });

        this.renderer.on('leaveNode', ({ node }) => {
            this.graph.setNodeAttribute(node, 'highlighted', false);
            this.renderer.refresh();
        });

        this.renderer.on('clickStage', () => {
            this.hideNodeDetails();
        });

        // 搜索
        document.getElementById('searchBox').addEventListener('input', (e) => {
            this.search(e.target.value);
        });

        // 关闭按钮
        document.getElementById('closeBtn').addEventListener('click', () => {
            this.hideNodeDetails();
        });
    }

    createLegend() {
        const legendItems = document.getElementById('legendItems');
        const types = [...new Set(this.data.nodes.map(n => n.tag))].filter(t => t);

        types.forEach(type => {
            const item = document.createElement('div');
            item.className = 'legend-item';
            item.innerHTML = `
                <div class="legend-dot" style="background: ${this.typeColors[type] || this.typeColors['UNKNOWN']}"></div>
                <span>${type}</span>
            `;
            legendItems.appendChild(item);
        });
    }

    createClusters() {
        const clustersList = document.getElementById('clustersList');
        const typeGroups = {};

        this.data.nodes.forEach(node => {
            if (!typeGroups[node.tag]) {
                typeGroups[node.tag] = [];
            }
            typeGroups[node.tag].push(node);
        });

        Object.entries(typeGroups).forEach(([type, nodes]) => {
            const item = document.createElement('div');
            item.className = 'cluster-item';
            item.innerHTML = `
                <div class="cluster-color" style="background: ${this.typeColors[type] || this.typeColors['UNKNOWN']}"></div>
                <div class="cluster-info">
                    <div class="cluster-name">${type}</div>
                    <div class="cluster-count">${nodes.length} 个节点</div>
                </div>
            `;
            item.addEventListener('click', () => this.filterByType(type));
            clustersList.appendChild(item);
        });
    }

    filterByType(type) {
        this.graph.forEachNode((node, attrs) => {
            if (attrs.tag === type) {
                this.graph.setNodeAttribute(node, 'highlighted', true);
            } else {
                this.graph.setNodeAttribute(node, 'hidden', true);
            }
        });
        this.renderer.refresh();

        // 3秒后恢复
        setTimeout(() => {
            this.graph.forEachNode((node) => {
                this.graph.setNodeAttribute(node, 'hidden', false);
                this.graph.setNodeAttribute(node, 'highlighted', false);
            });
            this.renderer.refresh();
        }, 3000);
    }

    search(query) {
        if (!query.trim()) {
            this.graph.forEachNode((node) => {
                this.graph.setNodeAttribute(node, 'highlighted', false);
            });
            this.renderer.refresh();
            return;
        }

        const lowerQuery = query.toLowerCase();
        let found = false;

        this.graph.forEachNode((node, attrs) => {
            if (attrs.label.toLowerCase().includes(lowerQuery)) {
                this.graph.setNodeAttribute(node, 'highlighted', true);
                if (!found) {
                    this.focusNode(node);
                    found = true;
                }
            } else {
                this.graph.setNodeAttribute(node, 'highlighted', false);
            }
        });

        this.renderer.refresh();
    }

    showNodeDetails(nodeId) {
        const attrs = this.graph.getNodeAttributes(nodeId);

        document.getElementById('nodeTitle').textContent = attrs.label;
        document.getElementById('nodeType').textContent = attrs.tag || '未知';
        document.getElementById('nodeDescription').textContent = attrs.description || '暂无描述';

        // 显示关联
        const connections = this.graph.edges(nodeId);
        const connectionList = document.getElementById('connectionList');

        connectionList.innerHTML = '';

        if (connections.length > 0) {
            connections.slice(0, 10).forEach(edge => {
                const [source, target] = this.graph.extremities(edge);
                const targetNode = source === nodeId ? target : source;
                const targetAttrs = this.graph.getNodeAttributes(targetNode);
                const edgeAttrs = this.graph.getEdgeAttributes(edge);

                const item = document.createElement('div');
                item.className = 'connection-item';
                item.innerHTML = `
                    <span class="connection-arrow">→</span>
                    <span>${targetAttrs.label}</span>
                `;
                connectionList.appendChild(item);
            });
        } else {
            connectionList.innerHTML = '<div class="connection-item">无直接关联</div>';
        }

        document.getElementById('nodeDetails').classList.add('show');

        // 高亮节点及邻居
        const neighbors = new Set(this.graph.neighbors(nodeId));
        neighbors.add(nodeId);

        this.graph.forEachNode((node) => {
            this.graph.setNodeAttribute(node, 'highlighted', neighbors.has(node));
        });

        this.renderer.refresh();
    }

    hideNodeDetails() {
        document.getElementById('nodeDetails').classList.remove('show');
        this.graph.forEachNode((node) => {
            this.graph.setNodeAttribute(node, 'highlighted', false);
        });
        this.renderer.refresh();
    }

    focusNode(nodeId) {
        const attrs = this.graph.getNodeAttributes(nodeId);
        this.renderer.getCamera().animate(
            { x: attrs.x, y: attrs.y, ratio: 0.5 },
            { duration: 600, easing: 'quadraticInOut' }
        );
    }

    showError(message) {
        document.getElementById('loading').innerHTML = `
            <div style="color: #f44336;">❌ ${message}</div>
        `;
    }
}

// 初始化
window.addEventListener('load', () => {
    new GraphViz();
});
