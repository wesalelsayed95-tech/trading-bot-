#include <iostream>
#include <string>
#include <chrono>
#include <stdexcept>
#include <curl/curl.h>

const std::string SOLANA_RPC_ENDPOINT = "https://api.mainnet-beta.solana.com";

struct RawTransaction {
    std::string senderPublicKey;
    std::string recipientPublicKey;
    uint64_t lamports;
    std::string blockhash;
    std::string signature;
};

size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* userp) {
    userp->append((char*)contents, size * nmemb);
    return size * nmemb;
}

class SolanaCoreProtocol {
private:
    CURL* curlHandle;

public:
    SolanaCoreProtocol() {
        curl_global_init(CURL_GLOBAL_DEFAULT);
        curlHandle = curl_easy_init();
        if (!curlHandle) {
            throw std::runtime_error("Failed to initialize CURL context.");
        }
    }

    ~SolanaCoreProtocol() {
        if (curlHandle) {
            curl_easy_cleanup(curlHandle);
        }
        curl_global_cleanup();
    }

    std::string sendRawRpcRequest(const std::string& jsonPayload) {
        std::string responseBuffer;

        if (curlHandle) {
            struct curl_slist* headers = nullptr;
            headers = curl_slist_append(headers, "Content-Type: application/json");

            curl_easy_setopt(curlHandle, CURLOPT_URL, SOLANA_RPC_ENDPOINT.c_str());
            curl_easy_setopt(curlHandle, CURLOPT_POSTFIELDS, jsonPayload.c_str());
            curl_easy_setopt(curlHandle, CURLOPT_HTTPHEADER, headers);
            curl_easy_setopt(curlHandle, CURLOPT_WRITEFUNCTION, WriteCallback);
            curl_easy_setopt(curlHandle, CURLOPT_WRITEDATA, &responseBuffer);
            curl_easy_setopt(curlHandle, CURLOPT_TIMEOUT_MS, 50L);

            CURLcode res = curl_easy_perform(curlHandle);
            if (res != CURLE_OK) {
                std::cerr << "[RPC TRANSMISSION ERROR] " << curl_easy_strerror(res) << std::endl;
            }

            curl_slist_free_all(headers);
        }
        return responseBuffer;
    }

    std::string fetchLatestBlockhash() {
        std::string payload = "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getLatestBlockhash\",\"params\":[{\"commitment\":\"processed\"}]}";
        return sendRawRpcRequest(payload);
    }
};

int main() {
    try {
        auto startTime = std::chrono::high_resolution_clock::now();

        SolanaCoreProtocol protocol;
        std::string blockhashResponse = protocol.fetchLatestBlockhash();

        auto endTime = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> latency = endTime - startTime;

        std::cout << "[BLOCKHASH DATA] " << blockhashResponse << std::endl;
        std::cout << "[EXECUTION LATENCY] " << latency.count() << " ms" << std::endl;

    } catch (const std::exception& e) {
        std::cerr << "[FATAL ERROR] " << e.what() << std::endl;
    }

    return 0;
}
