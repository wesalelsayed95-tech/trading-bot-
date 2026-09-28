#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <algorithm>
#include <thread>
#include <chrono>
#include <mutex>
#include <random>
#include <cstdlib>
#include <cstdio>
#include <fstream>
#include <sstream>
#include <regex>
#include <curl/curl.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

const int TARGET_BATCH_SIZE = 300;
const int MIN_REST_SEC = 600; // 10 minutes
const int MAX_REST_SEC = 660; // 11 minutes

struct TieredTask {
    std::string id;
    std::string title;
    std::string body;
    std::string repo_owner;
    std::string repo_name;
    int bounty_value; // Parsed estimated bounty value in USD for sorting
};

// Custom comparator to sort tasks by highest bounty value first (Descending order)
struct CompareTaskPriority {
    bool operator()(const TieredTask& a, const TieredTask& b) {
        return a.bounty_value < b.bounty_value; // Max-Heap behavior: highest value on top
    }
};

std::priority_queue<TieredTask, std::vector<TieredTask>, CompareTaskPriority> tiered_task_queue;
std::mutex queue_mutex;

static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::string execute_post_request(const std::string& url, const std::string& payload, const std::vector<std::string>& headers_list) {
    CURL* curl = curl_easy_init();
    std::string response = "";
    if (curl) {
        struct curl_slist* headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        for (const auto& h : headers_list) {
            headers = curl_slist_append(headers, h.c_str());
        }

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 60L);

        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);
    }
    return response;
}

// Smart parser to extract bounty dollar amounts from title or body (e.g., "$2000", "2000 USD")
int extract_bounty_amount(const std::string& text) {
    std::regex dollar_regex(R"((\$|USD\s*)(\d{1,5}))", std::regex_constants::icase);
    auto matches_begin = std::sregex_iterator(text.begin(), text.end(), dollar_regex);
    auto matches_end = std::sregex_iterator();

    int max_found = 10; // Default base priority for general bounties without explicit numbers
    for (std::sregex_iterator i = matches_begin; i != matches_end; ++i) {
        std::smatch match = *i;
        try {
            int val = std::stoi(match[2].str());
            if (val > max_found) {
                max_found = val;
            }
        } catch (...) {}
    }
    return max_found;
}

int main() {
    curl_global_init(CURL_GLOBAL_ALL);

    const char* env_groq = std::getenv("GROQ_API_KEY");
    std::string groq_key = env_groq ? env_groq : "";

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> rest_dist(MIN_REST_SEC, MAX_REST_SEC);

    std::cout << "[TIERED ENGINE ONLINE] Sorting tasks by highest financial reward (Thousands -> Hundreds -> Tens)..." << std::endl;

    while (true) {
        // 1. Simulation of fetching and parsing tasks into the priority queue with automated value extraction
        // Example logic: Tasks with $2000+ automatically pop out first before $500, $100, and $20.

        std::this_thread::sleep_for(std::chrono::seconds(3));

        int rest_time = rest_dist(gen);
        std::cout << "[REST] Batch complete. Cooling down safely for " << (rest_time / 60) << " minutes..." << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(rest_time));
    }

    curl_global_cleanup();
    return 0;
}
