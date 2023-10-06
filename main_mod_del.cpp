#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <assert.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>
#include <algorithm>
#include <string>
#include "nlohmann/json.hpp"
#include <fstream>

using namespace std;

#define NUM_THREADS 4
#define LINES 99161

using json = nlohmann::json;

struct JsonObject {
    std::vector<int> input_ids;
    std::vector<int> attention_mask;
};

struct Cell {
    int distance;
    int source_x, source_y; //if diff we use both, else we use only targer
};

template<typename T>
void print_vector(const std::vector<T>& vec) {
    std::cout << "[";
    for (size_t i = 0; i < vec.size(); ++i) {
        std::cout << vec[i];
        if (i < vec.size() - 1) {
            std::cout << ", ";
        }
    }
    std::cout << "]" << std::endl;
}


void number_adds(std::vector<int>vec) {
    for (size_t i = 0; i < vec.size(); ++i) {
        std::cout << vec[i];
        if (i < vec.size() - 1) {
            std::cout << ", ";
        }
    }
}


void print_matrix(std::vector<std::vector<Cell>> d, int lenS, int lenT) {

    int maxWidth = 0;
    for (int i = 0; i < lenS; ++i) {
        for (int j = 0; j < lenT; ++j) {
            int currentWidth = snprintf(NULL, 0, "%d", d[i][j].distance);
            if (currentWidth > maxWidth) {
                maxWidth = currentWidth;
            }
        }
    }


    for(int i = 0; i < lenS; i++) {
        for (int j = 0; j < lenT; j++){
            printf("%*d ", maxWidth, d[i][j].distance);
        }
        printf("\n");
    }

    for(int i = 0; i < lenS; i++) {
        for (int j = 0; j < lenT; j++){
            printf("[%d %d] ", d[i][j].source_x, d[i][j].source_y);
        }
        printf("\n");
    }

}

std::vector<int> process_vector(const std::vector<int>& input) {
    std::vector<int> output;
    bool contiguous_three = false;

    for (size_t i = 0; i < input.size(); ++i) {
        if (input[i] == 3) {
            contiguous_three = true;
        } else {
            if (contiguous_three) {
                output.push_back(1);
            } else {
                output.push_back(0);
            }
            contiguous_three = false;
        }
    }

    if (contiguous_three) {
        output.push_back(1);
    }

    return output;
}


std::vector<int> traverse_matrix(std::vector<std::vector<Cell>> d, int lenS, int lenT, const std::vector<int> source, const std::vector<int> target) {
    int x = lenS - 1;
    int y = lenT - 1;

    //printf("%d %d\n", x, y);

    std::vector<int> bucket;

    std::vector<int> add_mask;

    while( (x != 0) && (y != 0) ){

        int prev_x = d[x][y].source_x;
        int prev_y = d[x][y].source_y;

        int opp;  // 0 nothing, 1 dif, 2 del, 3 add
        //printf("%d %d\n", d[x][y].distance, d[prev_x][prev_y].distance);

        if((prev_x == x - 1) && (prev_y == y - 1)){
            opp = 1;
        }

        if((prev_x == x - 1) && (prev_y == y)){
            opp = 2;
        }

        if((prev_x == x) && (prev_y == y - 1)){
            opp = 3;
        }

        if((d[x][y].distance == d[prev_x][prev_y].distance) && (prev_x == x - 1) && (prev_y == y - 1)) {
            opp = 0;
        }

        bucket.push_back(opp);
        //printf("%d %d\n", d[x][y].source_x, d[x][y].source_y);

        x = prev_x;
        y = prev_y;
    }

    while (x != 0) {
        bucket.push_back(2); // deletion
        x--;
    }

    while (y != 0) {
        bucket.push_back(3); // insertion
        y--;
    }

    //print_vector(bucket);


    std::reverse(bucket.begin(), bucket.end());

    //print_vector(source);
    //print_vector(target);
    //print_vector(bucket);

    add_mask = process_vector(bucket);
    
    //print_vector(add_mask);

    for (size_t i = 0; i < target.size(); ++i) {
        //std::cout << target[i];
        if(bucket[i] == 3) {
            //std::cout << target[i] << ", ";
        }
    }
    //std::cout << endl;


    bucket.erase(std::remove_if(bucket.begin(), bucket.end(), [](int x) { return x == 3; }), bucket.end());

    //print_vector(bucket);
    
    return bucket;

}

std::vector<int> diff_finder(std::vector<int> source, std::vector<int> target) {
    //std::cout << source.size() << " " << target.size() << std::endl;
    int lenS = source.size() + 1;
    int lenT = target.size() + 1;

    std::vector<std::vector<Cell>> d(lenS, std::vector<Cell>(lenT));


    for (int i = 0; i < lenS; i++) {
        for (int j = 0; j < lenT; j++) {
            d[i][j].distance = 0;
            d[i][j].source_x = -1;
            d[i][j].source_y = -1; 
        }    
    }

    for (int i = 0; i < lenT; i++) {
        d[0][i].distance = i;
        d[0][i].source_x = 0;
        d[0][i].source_y = i - 1; 
    }   

    for (int i = 0; i < lenS; i++) {
        d[i][0].distance = i;
        d[i][0].source_x = i - 1;
        d[i][0].source_y = 0; 
    }

    for (int i = 1; i < lenS; i++) {
        for (int j = 1; j < lenT; j++) {
            if(source[i - 1] == target[j - 1]){
                d[i][j].distance = d[i - 1][j - 1].distance;
                d[i][j].source_x = i - 1;
                d[i][j].source_y = j - 1;
            } else {
                int insert_cost = d[i][j - 1].distance + 1;
                int del_cost = d[i - 1][j].distance + 1;
                int sub_cost = d[i - 1][j - 1].distance + 1;
                int min_cost = std::min({del_cost, sub_cost, insert_cost});

                std::string chosen_operation;

                if (min_cost == del_cost) {
                    chosen_operation = "deletion";
                } else if (min_cost == sub_cost) {
                    chosen_operation = "substitution";
                } else {
                    chosen_operation = "insertion";
                }

                d[i][j].distance = min_cost;

                if(chosen_operation == "substitution") {
                    d[i][j].source_x = i - 1;
                    d[i][j].source_y = j - 1;
                }

                if(chosen_operation == "deletion") {
                    d[i][j].source_x = i - 1;
                    d[i][j].source_y = j;
                }

                if(chosen_operation == "insertion") {
                    d[i][j].source_x = i;
                    d[i][j].source_y = j - 1;
                }
            }
        }    
    }

    //print_matrix(d, lenS, lenT);

    //std::vector<int> bucket = traverse_matrix(d, lenS, lenT);

    //create_json(source, bucket);

    return traverse_matrix(d, lenS, lenT, source, target); 
}

void create_json(std::vector<int> input_ids, std::vector<int> attention_mask, std::vector<int> labels){
    nlohmann::ordered_json j;
    j["input_ids"] = input_ids;
    j["attention_mask"] = attention_mask;
    j["labels"] = labels;

    std::ofstream outfile("licenta\\golden_corpus_test.txt");
    outfile << j.dump() << std::endl;
    outfile.close();
}

int main(int argc, char *argv[]) {
    pthread_t threads[NUM_THREADS];
    int thread_args[NUM_THREADS];
    int i;
    int result_code;
        
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    FILE *myfile;
    char correct[1000000];
    char wrong[1000000];
    int max = 0;

    // Open file
    //myfile = fopen("corpus/results_2/wiki_dirty_gpt_100000_shuffled_inter_128.txt", "r");
    myfile = fopen("corpus/results_2/golden_corpus_128_filtered_well_formed_no_duplicates_inter.txt", "r");
    if (myfile == NULL)
    {
        printf("Cannot open file \n");
        exit(0);
    }

    std::ofstream outfile("corpus/results_2/golden_corpus_128_filtered_well_formed_no_duplicates_mod_del.txt");

    while (fgets(correct, 1000000, myfile) && fgets(wrong, 1000000, myfile))
    {
        //printf("%s\n%s\n", correct, wrong);

        max += 2;
        if (max > LINES * 2)
            break;
        
        auto parsed_correct = json::parse(correct);
        auto parsed_wrong = json::parse(wrong);

        JsonObject correct_obj;
        JsonObject wrong_obj;

        correct_obj.input_ids = parsed_correct["input_ids"].get<std::vector<int>>();
        correct_obj.attention_mask = parsed_correct["attention_mask"].get<std::vector<int>>();

        wrong_obj.input_ids = parsed_wrong["input_ids"].get<std::vector<int>>();
        wrong_obj.attention_mask = parsed_wrong["attention_mask"].get<std::vector<int>>();

        //we want to get from wrong to correct
        std::vector<int> labels = diff_finder(wrong_obj.input_ids, correct_obj.input_ids);

        //create_json(wrong_obj.input_ids, wrong_obj.attention_mask, labels);

        nlohmann::ordered_json j;
        j["input_ids"] = wrong_obj.input_ids;
        j["attention_mask"] = wrong_obj.attention_mask;
        j["labels"] = labels;

        outfile << j.dump() << std::endl;

        // Print the contents of the object to verify
        /*std::cout << "Input IDs:" << std::endl;
        for (int id : wrong_obj.input_ids) {
            std::cout << id << " ";
        }
        std::cout << std::endl;
        for (int id : correct_obj.input_ids) {
            std::cout << id << " ";
        }

        std::cout << std::endl << "Attention Mask:" << std::endl;
        for (int mask : wrong_obj.attention_mask) {
            std::cout << mask << " ";
        }
        std::cout << std::endl;
        for (int mask : correct_obj.attention_mask) {
            std::cout << mask << " ";
        }
        std::cout << std::endl;*/
    }

    fclose(myfile);
    outfile.close();
    printf("MAIN program has ended.\n");
    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    printf("The time was: %f\n", elapsed_time);
    return 0;
}