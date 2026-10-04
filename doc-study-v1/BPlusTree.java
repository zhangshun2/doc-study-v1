import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * 一个简单的B+树实现
 * 这是一个简化版本，仅用于演示B+树的基本概念
 * @param <K> 键类型，必须实现Comparable接口
 * @param <V> 值类型
 */
public class BPlusTree<K extends Comparable<K>, V> {
    
    // B+树的阶数，表示一个节点最多有多少个子节点
    private int order;
    
    // 根节点
    private Node root;
    
    // 构造函数
    public BPlusTree(int order) {
        if (order < 3) {
            throw new IllegalArgumentException("B+树的阶数至少为3");
        }
        this.order = order;
        this.root = new LeafNode();
    }
    
    /**
     * 插入键值对
     * @param key 键
     * @param value 值
     */
    public void insert(K key, V value) {
        // 从根节点开始插入
        Node newNode = root.insert(key, value);
        
        // 如果返回了新节点，说明根节点分裂了，需要创建新的根节点
        if (newNode != null) {
            InternalNode newRoot = new InternalNode();
            newRoot.keys.add(newNode.keys.get(0));
            newRoot.children.add(root);
            newRoot.children.add(newNode);
            root = newRoot;
        }
    }
    
    /**
     * 查找键对应的值
     * @param key 键
     * @return 值，如果键不存在则返回null
     */
    public V search(K key) {
        return root.search(key);
    }
    
    /**
     * 范围查询，返回键在[start, end]范围内的所有值
     * @param start 起始键（包含）
     * @param end 结束键（包含）
     * @return 范围内的所有值
     */
    public List<V> rangeSearch(K start, K end) {
        List<V> result = new ArrayList<>();
        root.rangeSearch(start, end, result);
        return result;
    }
    
    /**
     * 打印树结构（用于调试）
     */
    public void printTree() {
        root.printNode(0);
    }
    
    /**
     * 节点抽象类，是InternalNode和LeafNode的父类
     */
    abstract class Node {
        // 存储键
        List<K> keys;
        
        // 构造函数
        Node() {
            this.keys = new ArrayList<>();
        }
        
        // 抽象方法：插入键值对
        abstract Node insert(K key, V value);
        
        // 抽象方法：查找键对应的值
        abstract V search(K key);
        
        // 抽象方法：范围查询
        abstract void rangeSearch(K start, K end, List<V> result);
        
        // 抽象方法：打印节点（用于调试）
        abstract void printNode(int level);
        
        // 查找键在节点中的位置
        int findKeyPosition(K key) {
            int low = 0;
            int high = keys.size() - 1;
            int mid;
            
            while (low <= high) {
                mid = (low + high) / 2;
                int cmp = key.compareTo(keys.get(mid));
                
                if (cmp == 0) {
                    return mid;
                } else if (cmp < 0) {
                    high = mid - 1;
                } else {
                    low = mid + 1;
                }
            }
            
            return low;
        }
    }
    
    /**
     * 内部节点类，存储键和指向子节点的指针
     */
    class InternalNode extends Node {
        // 存储子节点
        List<Node> children;
        
        // 构造函数
        InternalNode() {
            super();
            this.children = new ArrayList<>();
        }
        
        @Override
        Node insert(K key, V value) {
            // 找到键应该插入的子节点位置
            int pos = findKeyPosition(key);
            if (pos > 0) pos--; // 调整为子节点索引
            
            // 在子节点中插入
            Node newChild = children.get(pos).insert(key, value);
            
            // 如果子节点没有分裂，直接返回null
            if (newChild == null) {
                return null;
            }
            
            // 子节点分裂了，将新子节点的第一个键插入到当前节点
            K newKey = newChild.keys.get(0);
            int insertPos = findKeyPosition(newKey);
            keys.add(insertPos, newKey);
            children.add(insertPos + 1, newChild);
            
            // 检查当前节点是否需要分裂
            if (children.size() > order) {
                return split();
            }
            
            return null;
        }
        
        @Override
        V search(K key) {
            int pos = findKeyPosition(key);
            if (pos > 0) pos--; // 调整为子节点索引
            return children.get(pos).search(key);
        }
        
        @Override
        void rangeSearch(K start, K end, List<V> result) {
            int pos = findKeyPosition(start);
            if (pos > 0) pos--; // 调整为子节点索引
            children.get(pos).rangeSearch(start, end, result);
        }
        
        @Override
        void printNode(int level) {
            System.out.println("Level " + level + " Internal Node: " + keys);
            for (Node child : children) {
                child.printNode(level + 1);
            }
        }
        
        // 分裂节点
        Node split() {
            int mid = keys.size() / 2;
            
            InternalNode newNode = new InternalNode();
            
            // 将后半部分的键和子节点移动到新节点
            newNode.keys.addAll(keys.subList(mid, keys.size()));
            newNode.children.addAll(children.subList(mid, children.size()));
            
            // 更新当前节点
            keys.subList(mid, keys.size()).clear();
            children.subList(mid, children.size()).clear();
            
            return newNode;
        }
    }
    
    /**
     * 叶子节点类，存储键和值
     */
    class LeafNode extends Node {
        // 存储值
        List<V> values;
        
        // 指向下一个叶子节点的指针（用于范围查询）
        LeafNode next;
        
        // 构造函数
        LeafNode() {
            super();
            this.values = new ArrayList<>();
            this.next = null;
        }
        
        @Override
        Node insert(K key, V value) {
            int pos = findKeyPosition(key);
            
            // 如果键已存在，更新值
            if (pos < keys.size() && keys.get(pos).equals(key)) {
                values.set(pos, value);
                return null;
            }
            
            // 插入新键值对
            keys.add(pos, key);
            values.add(pos, value);
            
            // 检查是否需要分裂
            if (keys.size() > order - 1) {
                return split();
            }
            
            return null;
        }
        
        @Override
        V search(K key) {
            int pos = findKeyPosition(key);
            
            // 如果找到键，返回对应的值
            if (pos < keys.size() && keys.get(pos).equals(key)) {
                return values.get(pos);
            }
            
            return null;
        }
        
        @Override
        void rangeSearch(K start, K end, List<V> result) {
            int pos = findKeyPosition(start);
            
            // 收集当前节点中在范围内的值
            while (pos < keys.size() && keys.get(pos).compareTo(end) <= 0) {
                result.add(values.get(pos));
                pos++;
            }
            
            // 如果还没到范围的末尾，继续在下一个叶子节点中查找
            if (next != null && pos == keys.size()) {
                next.rangeSearch(start, end, result);
            }
        }
        
        @Override
        void printNode(int level) {
            System.out.println("Level " + level + " Leaf Node: " + keys + " -> " + values);
        }
        
        // 分裂节点
        Node split() {
            int mid = keys.size() / 2;
            
            LeafNode newNode = new LeafNode();
            
            // 将后半部分的键和值移动到新节点
            newNode.keys.addAll(keys.subList(mid, keys.size()));
            newNode.values.addAll(values.subList(mid, values.size()));
            
            // 更新当前节点
            keys.subList(mid, keys.size()).clear();
            values.subList(mid, values.size()).clear();
            
            // 更新叶子节点链表
            newNode.next = this.next;
            this.next = newNode;
            
            return newNode;
        }
    }
    
    // 简单测试
    public static void main(String[] args) {
        // 创建一个阶数为4的B+树
        BPlusTree<Integer, String> tree = new BPlusTree<>(4);
        
        // 插入一些键值对
        tree.insert(10, "Value 10");
        tree.insert(20, "Value 20");
        tree.insert(5, "Value 5");
        tree.insert(15, "Value 15");
        tree.insert(30, "Value 30");
        tree.insert(25, "Value 25");
        tree.insert(35, "Value 35");
        tree.insert(7, "Value 7");
        tree.insert(3, "Value 3");
        
        // 打印树结构
        System.out.println("B+树结构：");
        tree.printTree();
        
        // 查找测试
        System.out.println("\n查找测试：");
        System.out.println("键 10 的值: " + tree.search(10));
        System.out.println("键 15 的值: " + tree.search(15));
        System.out.println("键 40 的值: " + tree.search(40)); // 不存在的键
        
        // 范围查询测试
        System.out.println("\n范围查询测试 [7, 25]：");
        List<String> result = tree.rangeSearch(7, 25);
        for (String value : result) {
            System.out.println(value);
        }
    }
}