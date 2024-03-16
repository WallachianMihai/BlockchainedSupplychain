package com.example.producergui.controller;

import com.example.producergui.service.DataRepository;
import com.example.producergui.model.Contract;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;

import java.awt.*;
import java.io.File;
import java.io.IOException;

public class ContractController
{
    @FXML
    private TableView<Contract> contractTable;

    @FXML
    private TableColumn<Contract, String> productCol;

    @FXML
    private TableColumn<Contract, String> customerCol;

    @FXML
    private TableColumn<Contract, String> quantityCol;

    public void initialize() throws IOException
    {
        productCol.setCellValueFactory(new javafx.scene.control.cell.PropertyValueFactory<>("product"));
        customerCol.setCellValueFactory(new javafx.scene.control.cell.PropertyValueFactory<>("company"));
        quantityCol.setCellValueFactory(new javafx.scene.control.cell.PropertyValueFactory<>("quantity"));

        contractTable.setItems(DataRepository.getInstance().contractData);
    }

    public void handleViewContract() throws IOException
    {
        Contract selectedContract = contractTable.getSelectionModel().getSelectedItem();
        if (selectedContract != null)
        {
            if (Desktop.isDesktopSupported())
            {
                EventQueue.invokeLater(() ->
                {
                    try
                    {
                        Desktop.getDesktop().open(new File(selectedContract.getContractPath()));
                    }
                    catch (IOException e)
                    {
                        System.err.println("Error opening contract: " + e.getMessage());
                        throw new RuntimeException(e);
                    }
                });
            }
        }
    }
}
