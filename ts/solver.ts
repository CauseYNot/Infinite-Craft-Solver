
import * as csv from 'csv-parser';
import * as fs from 'fs';
import { BinaryTreeNode } from './binary_tree_display';

interface Recipe {
    [product: string]: [string, string];
}

// Read recipes from CSV file
const recipes: Recipe = {};
fs.createReadStream('./formatted_recipes.csv')
    .pipe(csv({ separator: '|' }))
    .on('data', (row) => {
        const [ingr_one, ingr_two, product] = Object.values(row);
        recipes[product] = [ingr_one, ingr_two];
    });

/**
 * Solver function to build a binary tree of ingredients based on recipes
 * @param target - The target product to start building the tree
 * @returns The root of the binary tree
 */
function solver(target: string): BinaryTreeNode {
    const root = new BinaryTreeNode(target);
    const paths_to_go: BinaryTreeNode[] = [root];
    const logged: string[] = ['Water', 'Fire', 'Earth', 'Wind'];

    while (paths_to_go.length > 0) {
        const node = paths_to_go.pop()!;

        if (logged.includes(node.key)) {
            continue;
        }

        logged.push(node.key);
        const [ingredient_one, ingredient_two] = recipes[node.key.trim()];
        node.left = new BinaryTreeNode(ingredient_one);
        node.right = new BinaryTreeNode(ingredient_two);
        paths_to_go.push(node.right);
        paths_to_go.push(node.left);
    }

    return root;
}

