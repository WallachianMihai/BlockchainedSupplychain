package com.example.producergui.controller;

import com.example.producergui.service.DataRepository;
import com.example.producergui.model.Customer;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;

import java.io.IOException;

public class CustomerController
{
    @FXML
    private TableView<Customer> customerTable;

    @FXML
    private TableColumn<Customer, String> nameCol;

    @FXML
    private TableColumn<Customer, String> locationCol;

    private ObservableList<Customer> customerData;

    public void initialize() throws IOException
    {
        nameCol.setCellValueFactory(new javafx.scene.control.cell.PropertyValueFactory<>("name"));
        locationCol.setCellValueFactory(new javafx.scene.control.cell.PropertyValueFactory<>("location"));

        customerData = DataRepository.getInstance().customerData;

        customerTable.setItems(customerData);
    }
}
