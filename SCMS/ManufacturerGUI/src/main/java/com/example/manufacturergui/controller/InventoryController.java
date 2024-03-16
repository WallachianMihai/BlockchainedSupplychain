package com.example.manufacturergui.controller;

import com.example.manufacturergui.Service.DataRepository;
import com.example.manufacturergui.model.Customer;
import com.example.manufacturergui.model.Inventory;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;

import java.io.IOException;

public class InventoryController
{
    @FXML
    private TableView<Inventory> inventoryTable;
    @FXML
    private TableColumn<Inventory, String> productCol;

    @FXML
    private TableColumn<Inventory, String> quantityCol;

    public void initialize() throws IOException
    {
        productCol.setCellValueFactory(new javafx.scene.control.cell.PropertyValueFactory<>("productName"));
        quantityCol.setCellValueFactory(new javafx.scene.control.cell.PropertyValueFactory<>("quantity"));

        inventoryTable.setItems(DataRepository.getInstance().inventoryData);
    }
}
