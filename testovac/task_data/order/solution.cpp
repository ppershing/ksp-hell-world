#include <stdio.h>

struct node {
    int value;
    node *left;
    node *right;
};

node special;

node* parse_tree(){
    char tmp[100],tmp2[10];
    scanf("%s", tmp);
    node* n =new node();
    n->left = NULL;
    n->right = NULL;
    if (tmp[0] == ')') {
        return &special;
    } else
    if (tmp[0]=='(') {
        n->left = parse_tree();
        if (n->left == &special) {
            return NULL;
        }
        scanf("%s", tmp);
        n->right = parse_tree();
        scanf("%s", tmp2); // ')'
    } 
    int i;
    sscanf(tmp,"%d", &i);
    n->value = i;
    return n;
}

void print_tree(node* n){
    printf("%d\n", n->value);
    printf("(\n");
    if (n->left){
        print_tree(n->left);
    }
    printf(")\n");
    printf("(\n");
    if (n->right){
        print_tree(n->right);
    }
    printf(")\n");
}

int main(){
    print_tree(parse_tree());
}
