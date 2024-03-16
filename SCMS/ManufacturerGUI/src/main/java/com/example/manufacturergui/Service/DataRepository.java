package com.example.manufacturergui.Service;

import com.example.manufacturergui.model.Contract;
import com.example.manufacturergui.model.Customer;
import com.example.manufacturergui.model.Inventory;
import com.example.manufacturergui.model.Product;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import java.io.IOException;
import java.util.Objects;

public class DataRepository
{
    private static DataRepository instance = null;

    private DataRepository() throws IOException
    {
        getData();
    }

    public static synchronized DataRepository getInstance() throws IOException
    {
        if (instance == null)
        {
            try
            {
                instance = new DataRepository();
            }
            catch (IOException e)
            {
                throw new RuntimeException(e);
            }
        }

        return instance;
    }

    public ObservableList<Product> productData;
    public ObservableList<Inventory> inventoryData;
    public ObservableList<Customer> customerData;
    public ObservableList<Contract> contractData;

    public void getData() throws IOException
    {
        getProducts();
        getCustomers();
        getContracts();
        getInventory();
    }

    public void getProducts() throws IOException
    {
        productData = FXCollections.observableArrayList();

        String url = "http://localhost:5000/products";

        OkHttpClient client = new OkHttpClient();

        // Create a request object
        Request request = new Request.Builder()
                .url(url)
                .build();

        // Send the request and get the response
        try (Response response = client.newCall(request).execute())
        {

            if (response.isSuccessful())
            {
                String jsonData = response.body().string();

                System.out.println("Response body: " + jsonData);

                ObjectMapper mapper = new ObjectMapper();
                JsonNode rootNode = mapper.readTree(jsonData);
                if(rootNode.isArray())
                {
                    for (int i = 0; i < rootNode.size(); i++) {
                        JsonNode productNode = rootNode.get(i);

                        Integer id = productNode.has("id") ? productNode.get("id").asInt() : null;
                        String name = productNode.has("name") ? productNode.get("name").asText() : null;
                        String description = productNode.has("description") ? productNode.get("description").asText() : null;
                        Double price = productNode.has("price") ? productNode.get("price").asDouble() : null;

                        productData.add(new Product(id, name, description, price));
                    }
                }
            }
            else
            {
                System.out.println("Error: " + response);
            }
        }
    }

    public void getCustomers() throws IOException
    {
        customerData = FXCollections.observableArrayList();

        String url = "http://localhost:5000/customers";

        OkHttpClient client = new OkHttpClient();

        // Create a request object
        Request request = new Request.Builder()
                .url(url)
                .build();

        // Send the request and get the response
        try (Response response = client.newCall(request).execute())
        {

            if (response.isSuccessful())
            {
                String jsonData = response.body().string();

                System.out.println("Response body: " + jsonData);

                ObjectMapper mapper = new ObjectMapper();
                JsonNode rootNode = mapper.readTree(jsonData);
                if (rootNode.isArray())
                {
                    for (int i = 0; i < rootNode.size(); i++)
                    {
                        JsonNode productNode = rootNode.get(i);

                        Integer id = productNode.has("id") ? productNode.get("id").asInt() : null;
                        String name = productNode.has("name") ? productNode.get("name").asText() : null;
                        String location = productNode.has("location") ? productNode.get("location").asText() : null;

                        customerData.add(new Customer(id, name, location));
                    }
                }
            }
            else
            {
                System.out.println("Error: " + response);
            }
        }
    }

    public void getContracts() throws IOException
    {
        contractData = FXCollections.observableArrayList();

        String url = "http://localhost:5000/contracts";

        OkHttpClient client = new OkHttpClient();

        // Create a request object
        Request request = new Request.Builder()
                .url(url)
                .build();

        // Send the request and get the response
        try (Response response = client.newCall(request).execute())
        {

            if (response.isSuccessful())
            {
                String jsonData = response.body().string();

                System.out.println("Response body: " + jsonData);

                ObjectMapper mapper = new ObjectMapper();
                JsonNode rootNode = mapper.readTree(jsonData);
                if(rootNode.isArray())
                {
                    for (int i = 0; i < rootNode.size(); i++) {
                        JsonNode contractNode = rootNode.get(i);

                        Integer id = contractNode.has("id") ? contractNode.get("id").asInt() : null;
                        Integer product_id = contractNode.has("product_id") ? contractNode.get("product_id").asInt() : null;
                        Integer customer_id = contractNode.has("customer_id") ? contractNode.get("customer_id").asInt() : null;
                        Integer quantity = contractNode.has("quantity") ? contractNode.get("quantity").asInt() : null;
                        String contract_path = contractNode.has("contract_path") ? contractNode.get("contract_path").asText() : null;

                        String product = getProductById(product_id).getName();
                        String customer = getCustomerById(customer_id).getName();

                        contractData.add(new Contract(id, customer, product, quantity, contract_path));
                    }
                }
            }
            else
            {
                System.out.println("Error: " + response);
            }
        }
    }

    public void getInventory() throws IOException
    {
        inventoryData = FXCollections.observableArrayList();

        String url = "http://localhost:5000/inventory";

        OkHttpClient client = new OkHttpClient();

        // Create a request object
        Request request = new Request.Builder()
                .url(url)
                .build();

        // Send the request and get the response
        try (Response response = client.newCall(request).execute())
        {

            if (response.isSuccessful())
            {
                String jsonData = response.body().string();

                System.out.println("Response body: " + jsonData);

                ObjectMapper mapper = new ObjectMapper();
                JsonNode rootNode = mapper.readTree(jsonData);
                if(rootNode.isArray())
                {
                    for (int i = 0; i < rootNode.size(); i++) {
                        JsonNode inventoryNode = rootNode.get(i);

                        Integer id = inventoryNode.has("id") ? inventoryNode.get("id").asInt() : null;
                        Integer product_id = inventoryNode.has("product_id") ? inventoryNode.get("product_id").asInt() : null;
                        Integer quantity = inventoryNode.has("quantity") ? inventoryNode.get("quantity").asInt() : null;

                        String product = getProductById(product_id).getName();
                        inventoryData.add(new Inventory(id, product, quantity));
                    }
                }
            }
            else
            {
                System.out.println("Error: " + response);
            }
        }
    }

    public Product getProductById(Integer id)
    {
        for (Product product : productData)
        {
            if(Objects.equals(product.getId(), id))
                return product;
        }
        return null;
    }

    public Customer getCustomerById(Integer id)
    {
        for (Customer customer : customerData)
        {
            if(Objects.equals(customer.getId(), id))
                return customer;
        }
        return null;
    }
}
