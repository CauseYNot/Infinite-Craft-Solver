class BinaryTreeNode {
    key: any;
    left: BinaryTreeNode | null;
    right: BinaryTreeNode | null;
    id: string | null;

    constructor(key: any, left: BinaryTreeNode | null = null, right: BinaryTreeNode | null = null) {
        this.key = key;
        this.left = left;
        this.right = right;
        this.id = null;
    }

    to_dot(dot_filepath: string, rankdir: string): void {
        let nodes_lines = `\t"${this.key}" [label=${this.key}, fontname="Roboto", shape="rectangle", style="rounded", root=true]\n`;
        let edges_lines = '';

        let to_visit: BinaryTreeNode[] = [this];
        this.id = this.key;

        let usedids: string[] = [this.id];
        while (to_visit.length > 0) {
            let node = to_visit.pop();
            let left = node.left;
            let right = node.right;
            if (left) {
                let leftid = left.key;
                while (usedids.includes(leftid)) {
                    leftid += '_';
                }
                left.id = leftid;
                usedids.push(left.id);

                nodes_lines += `\t"${left.id}" [label="${left.key}", fontname="Roboto", shape="rectangle", style="rounded"]\n`;
                edges_lines += `\t"${node.id}" -> "${left.id}" [dir="back"]\n`;

                to_visit.unshift(left);
            }
            if (right) {
                let rightid = right.key;
                while (usedids.includes(rightid)) {
                    rightid += '_';
                }
                right.id = rightid;
                usedids.push(right.id);

                nodes_lines += `\t"${right.id}" [label="${right.key}", fontname="Roboto", shape="rectangle", style="rounded"]\n`;
                edges_lines += `\t"${node.id}" -> "${right.id}" [dir="back"]\n`;

                to_visit.unshift(right);
            }
        }

        const fs = require('fs');
        fs.writeFileSync(dot_filepath, 'digraph tree {\n');
        fs.appendFileSync(dot_filepath, `\trankdir=${rankdir}\n`);
        fs.appendFileSync(dot_filepath, nodes_lines);
        fs.appendFileSync(dot_filepath, '\n');
        fs.appendFileSync(dot_filepath, edges_lines);
        fs.appendFileSync(dot_filepath, '}');
    }
}
