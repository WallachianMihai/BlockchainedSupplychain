package com.example.manufacturergui.controller;

import com.example.manufacturergui.Service.DataRepository;
import com.example.manufacturergui.model.Product;
import com.fasterxml.jackson.databind.JsonNode;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import okhttp3.*;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;

public class ProductController
{

    @FXML
    private TableView<Product> productTable;

    @FXML
    private TableColumn<Product, String> nameCol;

    @FXML
    private TableColumn<Product, String> priceCol;

    @FXML
    private Label productDescriptionLabel;

    private ObservableList<Product> productData;

    public void initialize() throws IOException
    {
        productData = FXCollections.observableArrayList();
        nameCol.setCellValueFactory(new javafx.scene.control.cell.PropertyValueFactory<>("name"));
        priceCol.setCellValueFactory(new javafx.scene.control.cell.PropertyValueFactory<>("price"));

        productData = DataRepository.getInstance().productData;

        productTable.setItems(productData);

        productTable.getSelectionModel().selectedItemProperty().addListener(
                (observable, oldValue, newValue) -> handleProductSelection(newValue));
    }

    private void handleProductSelection(Product selectedProduct)
    {
        if (selectedProduct != null)
        {
            productDescriptionLabel.setText(selectedProduct.getDescription());
        }
        else
        {
            productDescriptionLabel.setText("");
        }
    }
}
